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
    intent: Optional[Union[ChatIntent, LearnIntent, InfluenceIntent, GoTalkToIntent, NewRumorIntent]] = Field(
        default=None, description="One of the intent classes or None"
    )
    npc_response_to_player: str = Field(description="The NPC's concise response to the player, in character.")
    trust_change: int = Field(ge=-1000, le=1000, default=0)
    anger_change: int = Field(ge=-1000, le=1000, default=0)
    animosity_change: int = Field(ge=-1000, le=1000, default=0)
