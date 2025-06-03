import os
import json
import datetime
import time
import uuid
import inspect # Added for checking if something is a class
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from openai import OpenAI
from dotenv import load_dotenv

from simulation.llm_helper import LLMResponse

# Load environment variables from .env file
load_dotenv()
# Initialize OpenAI client
# It will automatically pick up OPENAI_API_KEY from environment variables
client = OpenAI()

LLM_LOG_FILE = "llm_calls.jsonl"
DEFAULT_MODEL = "gpt-4.1-nano-2025-04-14"


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


# --- Main LLM Interaction Function ---
def get_llm_response(prompt, model_name: str = DEFAULT_MODEL) -> Optional[LLMResponse]:

    request_payload = {
        'model': model_name,
        'input': prompt,
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

    # Example call
    # Make sure OPENAI_API_KEY is set in your .env file in the project root
    # (e.g., /c%3A/Users/fedse/Documents/Github/PartyFightInstigator/.env)
    # if os.getenv("OPENAI_API_KEY"):
    # player_input = "You seem a bit down today, everything okay?"
    #     llm_result = get_llm_response(
    #         npc_person_obj=mock_npc,
    #         player_utterance=player_input,
    #         trust_with_player=750,
    #         animosity_with_player=50
    #     )