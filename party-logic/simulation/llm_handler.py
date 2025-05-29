import os
import json
import datetime
import time
import uuid
import inspect # Added for checking if something is a class
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

if TYPE_CHECKING:
    from simulation.person import Person
    from simulation.npcsecret import NPCSecret

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
# It will automatically pick up OPENAI_API_KEY from environment variables
client = OpenAI()

LLM_LOG_FILE = "llm_calls.jsonl"
DEFAULT_MODEL = "gpt-4.1-nano-2025-04-14"

# --- Pydantic Models for LLM Structured Output ---

class RumorDetail(BaseModel):
    subjects: List[str] = Field(description="List of names of individuals the rumor is about.")
    originators: List[str] = Field(description="List of names of individuals who started or spread the rumor.")
    harmfulness: int = Field(ge=0, le=1000, description="Harmfulness of the rumor (0-1000).")
    plausibility: int = Field(ge=0, le=1000, description="Plausibility of the rumor (0-1000).")
    believed_by_npc: bool = Field(description="Did the NPC believe the rumor?")

class LLMResponse(BaseModel):
    trust_change: int = Field(ge=-1000, le=1000, description="Change in trust towards the player (-1000 to 1000). This should reflect belief/disbelief in any new rumors.")
    anger_change: int = Field(ge=-1000, le=1000, description="Change in anger (-1000 to 1000).")
    animosity_change: int = Field(ge=-1000, le=1000, description="Change in animosity towards the player (-1000 to 1000).")
    new_rumor_detected: Optional[RumorDetail] = Field(default=None, description="Details of a new rumor if one was identified from player's input.")
    npc_response_to_player: str = Field(description="The NPC's concise response to the player, in character.")

# --- LLM Call Logging ---

def log_llm_call(
    model_name: str,
    input_tokens: int,
    output_tokens: int,
    total_tokens: int,
    cost: float,
    status: str,
    response_time_ms: int,
    request_payload: Dict[str, Any],
    response_payload: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None
):
    # Create a deep copy to avoid modifying the original dictionary, 
    # especially if it contains mutable structures like lists or other dicts.
    # However, for this specific case, if request_payload is relatively flat 
    # and we are only modifying a potential class type to its name (string),
    # a shallow copy is usually sufficient and more performant.
    # If complex nested structures containing classes are possible, a more robust 
    # recursive sanitization might be needed.
    loggable_request_payload = request_payload.copy()

    # Sanitize fields that might contain non-serializable class types, like 'text_format'
    if 'text_format' in loggable_request_payload and inspect.isclass(loggable_request_payload['text_format']):
        loggable_request_payload['text_format'] = loggable_request_payload['text_format'].__name__

    # Sanitize response_payload if it's not None and potentially contains non-serializable content directly
    # (though current usage passes model_dump() or a dict with raw_content)
    # For now, assuming response_payload is already a dict or None as per current usage.

    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "model_name": model_name,
        "call_id": str(uuid.uuid4()),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost": cost, # Note: Actual cost calculation might need updated pricing.
        "status": status,
        "error_message": error_message,
        "response_time_ms": response_time_ms,
        "request_payload": loggable_request_payload, # Log the sanitized version
        "response_payload": response_payload
    }
    try:
        with open(LLM_LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f"Error writing to LLM log: {e}")

# --- Prompt Construction ---

def format_secrets_for_prompt(secrets: List['NPCSecret']) -> str:
    if not secrets:
        return "You currently have no notable secrets."
    
    return "\n".join([f"(Conceal Score: {s.conceal_score}/1000) - content: {s.text}" for s in secrets])


def construct_llm_prompt(
    npc_person_obj: 'Person',
    player_utterance: str,
    trust_with_player: int, # 0-1000
    animosity_with_player: int # 0-1000
) -> List[Dict[str, str]]:

    secrets_string = format_secrets_for_prompt(npc_person_obj.secrets if hasattr(npc_person_obj, 'secrets') else [])

    system_prompt = f"""
You are {getattr(npc_person_obj, 'name', 'this NPC')}, an NPC in a party simulation.
Your MBTI personality type is: {getattr(npc_person_obj, 'mbti', 'Unknown')}.
Your description: "{getattr(npc_person_obj, 'description', 'N/A')}".
Your current emotional state: Anger level is {getattr(npc_person_obj, 'anger', 0)}/1000.
Your traits: Gullibility is {getattr(npc_person_obj, 'gullibility', 0)}/1000, Gossip Level is {getattr(npc_person_obj, 'gossip_level', 0)}/1000.
Relationship with the player: Trust is {trust_with_player}/1000, Animosity is {animosity_with_player}/1000.
Known secrets about you (these are sensitive; your willingness to share depends on the player's tone, your relationship with them, and the secret's conceal_score):
{secrets_string}

Instructions for response:
1. Analyze the player's statement: and infer their tone
2. Based on this tone, your personality, your relationship with the player (trust/animosity), and the conceal_score of your secrets, decide on your response and any emotional changes.
3. If the player is inviting and friendly, and your trust in them is high while animosity is low, you may be more inclined to share a secret with a lower conceal_score.
4. If you detect the player is telling you a new rumor: assess its plausibility and harmfulness. Decide if you believe it. Your belief in a new rumor should positively influence your trust change towards the player; disbelief should negatively influence it. If a rumor is detected, include its details in the structured output.
5. Generate a response that is concise, in character, and try to make it funny and human-sounding.
6. Provide your response in the specified structure.
"""
    
    user_prompt_content = player_utterance

    return [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_prompt_content}
    ]

# --- Main LLM Interaction Function ---

def get_llm_response(
    npc_person_obj: 'Person',
    player_utterance: str,
    trust_with_player: int,
    animosity_with_player: int,
    model_name: str = DEFAULT_MODEL
) -> Optional[LLMResponse]:
    
    messages = construct_llm_prompt(
        npc_person_obj,
        player_utterance,
        trust_with_player,
        animosity_with_player,
    )

    request_payload = {
        'model': model_name,
        'input': messages,
        'text_format': LLMResponse # Pass the class directly as per user's preference
    }
    
    start_time = time.time()
    try:
        response = client.responses.parse(**request_payload)

        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)

        print(response)
        try:
            with open('resp.txt', 'w', encoding='utf-8') as f:
                f.write(str(response))
        except Exception as e:
            print("Failed to write response to file")

        parsed_response = response.output_parsed
        log_llm_call(
            model_name=model_name,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
            cost=0.0,
            status="success",
            response_time_ms=response_time_ms,
            request_payload=request_payload,
            response_payload=parsed_response.model_dump()  # Log the parsed Pydantic model as dict
        )
        return parsed_response

    except Exception as e:
        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)
        error_msg = f"Error calling OpenAI API: {e}"
        print(error_msg)
        log_llm_call(
            model_name=model_name,
            input_tokens=0, # Unlikely to have token counts if API call failed early
            output_tokens=0,
            total_tokens=0,
            cost=0.0,
            status="failure",
            response_time_ms=response_time_ms,
            request_payload=request_payload,
            error_message=error_msg
        )
        return None

if __name__ == '__main__':
    # This is a placeholder for testing.
    # You'll need to create mock objects for Person and NPCSecret that match your actual class structures.

    # --- Mock Objects (replace with your actual classes and instances) ---
    class MockNPCSecret:
        def __init__(self, text, conceal_score):
            self.text = text
            self.conceal_score = conceal_score

    class MockPerson:
        def __init__(self, id, name, mbti, description, anger, gullibility, gossip_level, secrets_list):
            self.id = id
            self.name = name
            self.mbti = mbti
            self.description = description
            self.anger = anger
            self.gullibility = gullibility
            self.gossip_level = gossip_level
            self.secrets = secrets_list # List of MockNPCSecret objects

    # Create a mock NPC
    npc_secret1 = MockNPCSecret(text="Afraid of ducks", conceal_score=200)
    npc_secret2 = MockNPCSecret(text="Secretly a millionaire", conceal_score=800)
    mock_npc = MockPerson(
        id="npc_jane_001",
        name="Jane Doe",
        mbti="INFJ",
        description="A quirky artist who loves to chat.",
        anger=100,
        gullibility=600,
        gossip_level=700,
        secrets_list=[npc_secret1, npc_secret2]
    )

    player_input = "I heard a Rumor that Keving cheated on Macy with Clara."
    # player_input = "You seem a bit down today, everything okay?"


    print(f"--- Simulating LLM call for NPC: {mock_npc.name} ---")
    
    # Example call
    # Make sure OPENAI_API_KEY is set in your .env file in the project root
    # (e.g., /c%3A/Users/fedse/Documents/Github/PartyFightInstigator/.env)
    if os.getenv("OPENAI_API_KEY"):
        llm_result = get_llm_response(
            npc_person_obj=mock_npc,
            player_utterance=player_input,
            trust_with_player=750,
            animosity_with_player=50
        )

    #     if llm_result:
    #         print("\n--- LLM Response Parsed ---")
    #         print(f"NPC Response: {llm_result.npc_response_to_player}")
    #         print(f"Trust Change: {llm_result.trust_change}")
    #         print(f"Anger Change: {llm_result.anger_change}")
    #         print(f"Animosity Change: {llm_result.animosity_change}")
    #         if llm_result.new_rumor_detected:
    #             print("New Rumor Detected:")
    #             print(f"  Subjects: {llm_result.new_rumor_detected.subjects}")
    #             print(f"  Originators: {llm_result.new_rumor_detected.originators}")
    #             print(f"  Harmfulness: {llm_result.new_rumor_detected.harmfulness}")
    #             print(f"  Plausibility: {llm_result.new_rumor_detected.plausibility}")
    #             print(f"  Believed by NPC: {llm_result.new_rumor_detected.believed_by_npc}")
    #         else:
    #             print("No new rumor detected.")
    #     else:
    #         print("\n--- LLM Call Failed ---")
    #         print("Check llm_calls.jsonl for details.")
    # else:
    #     print("\n--- Skipping LLM call: OPENAI_API_KEY not found in environment. ---")
    #     print("Please ensure your .env file is set up correctly at the project root.")
    #
    # print(f"\nLog file is at: {os.path.abspath(LLM_LOG_FILE)}")
    # You would integrate calls to get_llm_response() into your simulation's conversation logic. 