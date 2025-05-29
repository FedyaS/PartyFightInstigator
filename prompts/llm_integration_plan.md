# LLM Integration Plan

## 1. LLM Call Logging and Monitoring

*   **Objective:** Track LLM API calls for usage, cost, success/failure, and performance.
*   **Log File:** Create `llm_calls.jsonl` (JSON Lines format for easy parsing). Each line will be a JSON object representing a single API call.
*   **Log Structure (each line in `llm_calls.jsonl`):**
    ```json
    {
        "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
        "model_name": "gpt-4o-mini", // or whatever model is used
        "call_id": "unique_call_identifier",
        "prompt_tokens": 0, // number of tokens in the prompt
        "completion_tokens": 0, // number of tokens in the completion
        "total_tokens": 0, // total tokens
        "cost": 0.00, // estimated cost in USD
        "status": "success" | "failure",
        "error_message": null | "error details",
        "response_time_ms": 0, // duration of the API call in milliseconds
        "request_payload": { ... }, // summary or reference to the input
        "response_payload": { ... } // summary or reference to the output
    }
    ```
*   **Logging Function:**
    *   A utility function, likely in `llm_handler.py` or a new `llm_utils.py`.
    *   Takes necessary parameters (model, tokens, status, etc.).
    *   Appends a new log entry to `llm_calls.jsonl`.

## 2. OpenAI API Integration (gpt-4o-mini)

*   **Library:** Use the official `openai` Python library.
*   **API Key Management:**
    *   Store API key in a `.env` file at the project root: `OPENAI_API_KEY='your_key_here'`.
    *   Add `.env` to `.gitignore`.
    *   Load the key in Python using a library like `python-dotenv` (needs to be added to project dependencies).
*   **Structured Output (Pydantic):**
    *   Define Pydantic models for the expected LLM response structure (see Section 5).
    *   Use OpenAI's `client.responses.parse(model="<model_name>", input=[...], text_format=<PydanticModel>)` method to get structured JSON output conforming to these Pydantic models.

## 3. Secret Key Management

*   Store the OpenAI API key in a `.env` file at the project root (e.g., `/c%3A/Users/fedse/Documents/Github/PartyFightInstigator/.env`).
*   The file content should be: `OPENAI_API_KEY='your_actual_api_key_here'`.
*   Add `.env` to your `.gitignore` file to prevent committing the key.
*   Use a library like `python-dotenv` to load this key into the application environment at runtime.

## 4. Context Provisioning

*   **Objective:** Provide the LLM with relevant information about the NPC.
*   **Context String (Example Structure):**
    ```
    You are {person.name}, an NPC in a party simulation.
    Your MBTI personality type is: {person.mbti}.
    Your description: "{person.description}".
    Your current emotional state: Anger level is {person.anger}/1000.
    Your traits: Gullibility is {person.gullibility}/1000, Gossip Level is {person.gossip_level}/1000.
    Relationship with the player: Trust is {input_trust_with_player}/1000, Animosity is {input_animosity_with_player}/1000.
    Known secrets about you (these are sensitive; your willingness to share depends on the player's tone, your relationship, and the secret's conceal_score):
    {list_of_all_npc_secrets_with_their_conceal_scores} // LLM will decide if any are shared.
    Current conversation topic (if any): ...

    The player says to you: "{player_utterance}"

    Analyze the player's statement: infer their tone (e.g., friendly, neutral, hostile). Based on this tone, your personality, your relationship with the player (trust/animosity), and the conceal_score of your secrets, decide on your response and any emotional changes.
    If the player is inviting and friendly, and your trust in them is high while animosity is low, you may be more inclined to share a secret with a lower conceal_score.

    If you detect the player is telling you a new rumor: assess its plausibility and harmfulness. Decide if you believe it. Your belief in a new rumor should positively influence your trust change towards the player; disbelief should negatively influence it.

    Generate a response that is concise, in character, and try to make it funny and human-sounding.
    ```
*   **Details to Clarify/Add:**
    *   The player's direct relationship attributes (trust, animosity) with the NPC will be passed to the LLM context function.
    *   `gossip_level` is confirmed (0-1000) and assumed to be added to the `Person` class and its schema.
    *   Secrets: All of the NPC's secrets (instances of `NPCSecret` with their `conceal_score`) will be passed to the LLM. The LLM will be instructed to:
        *   Infer the player's tone from their utterance.
        *   Decide whether to reveal any secrets based on this inferred tone, current trust/animosity with the player, the NPC's personality, and the secret's `conceal_score`.
    *   The prompt will instruct the LLM to make its dialogue response "funny and human-sounding."
    *   The prompt will instruct the LLM that its `trust_change` output should be influenced by whether any new rumor detected from the player's input is believed or disbelieved.
    *   ~~Decision point: Pre-filter secrets before LLM call, or let LLM decide based on all secrets and context?~~ (Decision: Pass all secrets to LLM for now).

## 5. LLM Response Structure (to be enforced by Pydantic and OpenAI's functions/tools calling)

*   **Pydantic Model for LLM Output (`LLMResponse`):**
    ```python
    from pydantic import BaseModel, Field
    from typing import List, Optional

    class RumorDetail(BaseModel):
        subjects: List[str] = Field(description="List of names of individuals the rumor is about.")
        originators: List[str] = Field(description="List of names of individuals who started or spread the rumor.")
        harmfulness: int = Field(description="Harmfulness of the rumor (0-1000).")
        plausibility: int = Field(description="Plausibility of the rumor (0-1000).")
        believed_by_npc: bool = Field(description="Did the NPC believe the rumor?")

    class LLMResponse(BaseModel):
        trust_change: int = Field(description="Change in trust towards the player (-1000 to 1000). This should reflect belief/disbelief in any new rumors.")
        anger_change: int = Field(description="Change in anger (-1000 to 1000).")
        animosity_change: int = Field(description="Change in animosity towards the player (-1000 to 1000).")
        new_rumor_detected: Optional[RumorDetail] = Field(default=None, description="Details of a new rumor if one was identified from player's input.")
        npc_response_to_player: str = Field(description="The NPC's concise response to the player, in character.")
    ```
*   **Integration:**
    *   The main function in `llm_handler.py` will take the player's utterance and the NPC `Person` object.
    *   It will construct the prompt, call the OpenAI API (with structured output instruction referencing the Pydantic model).
    *   Parse the response using the Pydantic model.
    *   Log the call details.
    *   Return the parsed Pydantic object to the simulation logic (e.g., `NPCConvo` or `SimClass`).
*   **Details to Clarify/Add:**
    *   The `npc_response_to_player` should be generated in a style that is "funny and human-sounding" as per LLM instructions.
    *   If `new_rumor_detected` is populated, the simulation logic should use `new_rumor_detected.believed_by_npc` to determine if a `Rumor` game object is created.
    *   The `trust_change` returned by the LLM should already account for the belief/disbelief in a detected rumor.

## Open Questions & Next Steps:

1.  ~~**Player Representation:** How is the player character represented in the simulation? Is it a `Person` object? This is crucial for fetching relationship details.~~ (Addressed: Trust/animosity with player will be passed directly).
2.  ~~**`gossip_level`:** Confirm addition to `Person` class and schema. What's its range (0-1000)?~~ (Addressed: 0-1000, assumed added)
3.  **Secret Details in Prompt & NPC State:**
    *   Finalize criteria for sharing secrets (thresholds for good relationship, `conceal_score`). (LLM to decide based on context for now)
    *   Clarify how player tone is inferred and used by the LLM (see context provisioning notes).
    *   ~~Decision point: Pre-filter secrets before LLM call, or let LLM decide based on all secrets and context?~~ (Addressed: Pass all for now)
4.  **Error Handling:** Define strategies for API errors, parsing failures, or unexpected LLM outputs.
5.  **Location of LLM Call:** Where in the existing `simclass.py` or `npcconvo.py` logic will the call to the `llm_handler` module be made? (e.g., when a player interacts with an NPC).

Let's refine this! 