from pydantic import BaseModel
from typing import List, Optional

class ChatMessageRequest(BaseModel):
    message: str
    rep_id: int = 1
    chat_history: List[dict] = []

class ChatMessageResponse(BaseModel):
    reply: str
    extracted_fields: Optional[dict] = None
    suggested_followups: Optional[List[str]] = None
    tool_used: Optional[str] = None
    interaction_id: Optional[int] = None
    history: Optional[List[dict]] = None
