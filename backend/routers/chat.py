from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from schemas.chat import ChatMessageRequest, ChatMessageResponse
from agent.graph import crm_graph
from agent.tools.log_interaction import log_interaction_tool
from agent.tools.edit_interaction import edit_interaction_tool
from agent.tools.get_hcp_history import get_hcp_history_tool
from agent.tools.suggest_followups import suggest_followups_tool
from agent.tools.search_hcp import search_hcp_tool

router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
async def chat_message(
    body: ChatMessageRequest,
    session: AsyncSession = Depends(get_session)
):
    # Build initial state
    initial_state = {
        "user_input": body.message,
        "rep_id": body.rep_id,
        "chat_history": body.chat_history,
    }

    # Run LangGraph agent
    try:
        final_state = await crm_graph.ainvoke(initial_state)
    except Exception as e:
        print(f"Graph Invoke Error: {e}")
        return ChatMessageResponse(
            reply=f"⚠️ AI Graph Error: {str(e)}",
            tool_used="error"
        )

    tool = final_state.get("tool_to_call", "unknown")
    tool_result = {}
    interaction_id = None
    suggested_followups = final_state.get("suggested_followups", [])

    try:
        # Execute the appropriate tool with DB access
        if tool == "log":
            tool_result = await log_interaction_tool(final_state, session)
            interaction_id = tool_result.get("interaction_id")
            if not suggested_followups:
                suggested_followups = []

        elif tool == "edit":
            # Auto-fetch the most recent interaction if missing
            iid = final_state.get("interaction_id")
            if not iid:
                from sqlalchemy import text
                res = await session.execute(text("SELECT id FROM interactions ORDER BY id DESC LIMIT 1"))
                row = res.fetchone()
                iid = row[0] if row else None
                
            if iid:
                updates = {k: final_state.get(k) for k in [
                    "interaction_type", "interaction_date", "topics_discussed",
                    "sentiment", "outcomes", "follow_up_actions",
                    "materials_shared", "samples_distributed",
                ] if final_state.get(k) is not None}
                tool_result = await edit_interaction_tool(iid, updates, session)
            else:
                tool_result = {"error": "No interaction ID found to edit."}

        elif tool == "history":

            hcp_name = final_state.get("hcp_name") or body.message
            tool_result = await get_hcp_history_tool(hcp_name, session)

        elif tool == "followup":
            hcp_id = final_state.get("hcp_id")
            if hcp_id:
                tool_result = await suggest_followups_tool(hcp_id, body.message, session)
                suggested_followups = tool_result.get("suggested_followups", [])
            else:
                suggested_followups = final_state.get("suggested_followups", [])

        elif tool == "search":
            query = final_state.get("hcp_name") or body.message
            tool_result = await search_hcp_tool(query, session)
            
    except Exception as e:
        print(f"Tool Execution Error: {e}")
        tool_result = {"error": f"Tool failed: {str(e)}"}

    # Merge tool_result into final_state for formatting
    merged_state = {**final_state, "tool_result": tool_result}
    from agent.nodes import response_formatter_node
    merged_state = response_formatter_node(merged_state)

    # Build extracted fields to auto-populate the form
    extracted_fields = None
    if tool in ("log", "edit"):
        fields_to_map = {
            "hcp_name": "hcp_name",
            "interaction_type": "interaction_type",
            "interaction_date": "interaction_date",
            "interaction_time": "interaction_time",
            "attendees": "attendees",
            "topics_discussed": "topics_discussed",
            "materials_shared": "materials_shared",
            "samples_distributed": "samples_distributed",
            "sentiment": "sentiment",
            "outcomes": "outcomes",
            "follow_up_actions": "follow_up_actions"
        }
        extracted_fields = {k: final_state.get(v) for k, v in fields_to_map.items() if final_state.get(v) is not None}
        
        # If edit, only return the fields that were actually updated in final_state
        if tool == "edit":
            extracted_fields = {k: v for k, v in extracted_fields.items() if k in tool_result.get("updated_fields", [])}

    return ChatMessageResponse(
        reply=merged_state.get("reply", ""),
        extracted_fields=extracted_fields,
        suggested_followups=suggested_followups,
        tool_used=tool,
        interaction_id=interaction_id,
    )
