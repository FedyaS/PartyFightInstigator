from typing import Union, List, Optional, Dict, Any, TYPE_CHECKING
from pydantic import BaseModel, Field

class ChatIntent(BaseModel):
    pass

class LearnIntent(BaseModel):
    pass

class InfluencePerson(BaseModel):
    name: str = Field(description="Name of the NPC relationship being influenced")
    id: str = Field(description="ID of the NPC with whom relationship is being influenced")
    animosity_change: int = Field(ge=-1000, le=1000, default=0)
    trust_change: int = Field(ge=-1000, le=1000, default=0)

class InfluenceIntent(BaseModel):
    influences: List[InfluencePerson] = Field()

class GoTalkToIntent(BaseModel):
    name: str = Field(description="Name of NPC to go talk to")
    id: str = Field(description="ID of NPC to go talk to")

class LLMPerson(BaseModel):
    name: str = Field()
    id: str = Field()

class NewRumorIntent(BaseModel):
    text: str = Field(description="Text of the rumor")
    hash_text: str = Field(description="Hash text of the rumor to compare to other rumors")
    subjects: List[LLMPerson]
    originators: List[LLMPerson]
    plausibility: int = Field(ge=0, le=1000, default=500, description="How plausible is the rumor")
    harmfulness: int = Field(ge=0, le=1000, default=500, description="How harmful is the rumor")
    id_existing_rumor: Optional[str] = Field(description="ID of the existing rumor if this rumor matches it")

class LLMResponse(BaseModel):
    out_of_scope: bool = Field(description='users query is out of scope or you can not fulfill the request')
    chat_intent: Optional[ChatIntent] = Field(default=None, description="Chat intent if applicable")
    learn_intent: Optional[LearnIntent] = Field(default=None, description="Learn intent if applicable")
    influence_intent: Optional[InfluenceIntent] = Field(default=None, description="Influence intent if applicable")
    go_talk_to_intent: Optional[GoTalkToIntent] = Field(default=None, description="Go talk to intent if applicable")
    new_rumor_intent: Optional[NewRumorIntent] = Field(default=None, description="New rumor intent if applicable")
    npc_response_to_player: str = Field(description="The NPC's concise response to the player, in character.")
    trust_change: int = Field(ge=-1000, le=1000, default=0)
    anger_change: int = Field(ge=-1000, le=1000, default=0)
    animosity_change: int = Field(ge=-1000, le=1000, default=0)

# class RumorDetail(BaseModel):
#     subjects: List[str] = Field(description="List of names of individuals the rumor is about.")
#     originators: List[str] = Field(description="List of names of individuals who started or spread the rumor.")
#     harmfulness: int = Field(ge=0, le=1000, description="Harmfulness of the rumor (0-1000).")
#     plausibility: int = Field(ge=0, le=1000, description="Plausibility of the rumor (0-1000).")
#     believed_by_npc: bool = Field(description="Did the NPC believe the rumor?")
#
# class LLMResponse(BaseModel):
#     trust_change: int = Field(ge=-1000, le=1000, description="Change in trust towards the player (-1000 to 1000). This should reflect belief/disbelief in any new rumors.")
#     anger_change: int = Field(ge=-1000, le=1000, description="Change in anger (-1000 to 1000).")
#     animosity_change: int = Field(ge=-1000, le=1000, description="Change in animosity towards the player (-1000 to 1000).")
#     new_rumor_detected: Optional[RumorDetail] = Field(default=None, description="Details of a new rumor if one was identified from player's input.")
#     npc_response_to_player: str = Field(description="The NPC's concise response to the player, in character.")
