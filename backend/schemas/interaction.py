from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

class InteractionCreate(BaseModel):
    hcp_id: Optional[int] = None
    hcp_name: Optional[str] = None
    rep_id: int = 1
    interaction_type: Optional[str] = "Meeting"
    interaction_date: date
    interaction_time: Optional[time] = None
    attendees: Optional[List[str]] = []
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[str]] = []
    samples_distributed: Optional[List[str]] = []
    sentiment: Optional[str] = "Neutral"
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    raw_chat_input: Optional[str] = None

class InteractionUpdate(BaseModel):
    interaction_type: Optional[str] = None
    interaction_date: Optional[date] = None
    interaction_time: Optional[time] = None
    attendees: Optional[List[str]] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[List[str]] = None
    samples_distributed: Optional[List[str]] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None

class InteractionOut(BaseModel):
    id: int
    hcp_id: Optional[int]
    rep_id: int
    interaction_type: Optional[str]
    interaction_date: date
    interaction_time: Optional[time]
    attendees: Optional[str]
    topics_discussed: Optional[str]
    materials_shared: Optional[str]
    samples_distributed: Optional[str]
    sentiment: Optional[str]
    outcomes: Optional[str]
    follow_up_actions: Optional[str]
    ai_summary: Optional[str]
    ai_suggested_followups: Optional[str]

    class Config:
        from_attributes = True
