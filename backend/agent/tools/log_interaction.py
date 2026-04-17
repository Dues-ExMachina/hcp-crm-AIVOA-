import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from models.interaction import Interaction
from services.groq_service import generate_summary


async def log_interaction_tool(state: dict, session: AsyncSession) -> dict:
    """
    Tool 1: Logs a new HCP interaction to MySQL.
    Resolves HCP by name, generates AI summary, inserts record.
    """
    # 1. Resolve HCP ID by name
    hcp_id = state.get("hcp_id")
    if not hcp_id and state.get("hcp_name"):
        result = await session.execute(
            text("SELECT id FROM hcps WHERE name LIKE :name LIMIT 1"),
            {"name": f"%{state['hcp_name']}%"}
        )
        row = result.fetchone()
        hcp_id = row[0] if row else None

    # 2. Generate AI summary via Groq gemma2-9b-it
    ai_summary = await generate_summary(state)

    # 3. Insert interaction record
    interaction = Interaction(
        hcp_id=hcp_id,
        rep_id=state.get("rep_id", 1),
        interaction_type=state.get("interaction_type", "Meeting"),
        interaction_date=state.get("interaction_date"),
        interaction_time=state.get("interaction_time"),
        attendees=json.dumps(state.get("attendees") or []),
        topics_discussed=state.get("topics_discussed"),
        materials_shared=json.dumps(state.get("materials_shared") or []),
        samples_distributed=json.dumps(state.get("samples_distributed") or []),
        sentiment=state.get("sentiment", "Neutral"),
        outcomes=state.get("outcomes"),
        follow_up_actions=state.get("follow_up_actions"),
        ai_summary=ai_summary,
        ai_suggested_followups=json.dumps(state.get("suggested_followups") or []),
        raw_chat_input=state.get("user_input"),
    )
    session.add(interaction)
    await session.commit()
    await session.refresh(interaction)

    return {"interaction_id": interaction.id, "ai_summary": ai_summary, "status": "logged"}
