import json
from sqlalchemy.ext.asyncio import AsyncSession
from models.interaction import Interaction
from services.groq_service import generate_summary


async def edit_interaction_tool(interaction_id: int, updates: dict, session: AsyncSession) -> dict:
    """
    Tool 2: Edits an existing interaction record by ID.
    Only updates provided fields. Re-generates AI summary if key fields change.
    """
    interaction = await session.get(Interaction, interaction_id)
    if not interaction:
        return {"error": f"Interaction {interaction_id} not found", "status": "error"}

    allowed_fields = [
        "interaction_type", "interaction_date", "interaction_time",
        "attendees", "topics_discussed", "materials_shared",
        "samples_distributed", "sentiment", "outcomes", "follow_up_actions",
    ]
    changed_fields = []

    for field in allowed_fields:
        if field in updates and updates[field] is not None:
            # Serialize lists to JSON strings
            val = updates[field]
            if isinstance(val, list):
                val = json.dumps(val)
            setattr(interaction, field, val)
            changed_fields.append(field)

    # Re-summarize if meaningful content changed
    key_fields = {"topics_discussed", "outcomes", "sentiment"}
    if key_fields & set(changed_fields):
        interaction.ai_summary = await generate_summary({
            "hcp_name": None,
            "interaction_type": interaction.interaction_type,
            "interaction_date": str(interaction.interaction_date),
            "topics_discussed": interaction.topics_discussed,
            "sentiment": interaction.sentiment,
            "outcomes": interaction.outcomes,
            "follow_up_actions": interaction.follow_up_actions,
        })

    await session.commit()

    return {
        "interaction_id": interaction_id,
        "updated_fields": changed_fields,
        "status": "updated",
    }
