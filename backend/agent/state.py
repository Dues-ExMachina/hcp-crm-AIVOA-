from typing import TypedDict, Optional, List, Any

class AgentState(TypedDict, total=False):
    # Input
    user_input: str
    rep_id: int
    chat_history: List[dict]

    # Extracted interaction data
    hcp_name: Optional[str]
    hcp_id: Optional[int]
    interaction_type: Optional[str]
    interaction_date: Optional[str]
    interaction_time: Optional[str]
    attendees: Optional[List[str]]
    topics_discussed: Optional[str]
    materials_shared: Optional[List[str]]
    samples_distributed: Optional[List[str]]
    sentiment: Optional[str]
    outcomes: Optional[str]
    follow_up_actions: Optional[str]

    # Agent control
    tool_to_call: Optional[str]
    tool_result: Optional[Any]
    ai_summary: Optional[str]
    suggested_followups: Optional[List[str]]
    error: Optional[str]
    interaction_id: Optional[int]
    reply: Optional[str]
