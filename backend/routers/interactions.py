import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from core.database import get_session
from schemas.interaction import InteractionCreate, InteractionUpdate, InteractionOut
from models.interaction import Interaction
from services.groq_service import generate_summary

router = APIRouter()


@router.get("/")
async def list_interactions(
    hcp_id: int = None,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
):
    query = "SELECT * FROM interactions"
    params = {}
    if hcp_id:
        query += " WHERE hcp_id = :hcp_id"
        params["hcp_id"] = hcp_id
    query += " ORDER BY interaction_date DESC, created_at DESC LIMIT :limit"
    params["limit"] = limit
    result = await session.execute(text(query), params)
    rows = result.fetchall()
    return [dict(r._mapping) for r in rows]


@router.post("/", response_model=InteractionOut)
async def create_interaction(
    body: InteractionCreate,
    session: AsyncSession = Depends(get_session)
):
    # Resolve HCP ID if name provided but no ID
    hcp_id = body.hcp_id
    if not hcp_id and body.hcp_name:
        result = await session.execute(
            text("SELECT id FROM hcps WHERE name LIKE :name LIMIT 1"),
            {"name": f"%{body.hcp_name}%"}
        )
        row = result.fetchone()
        hcp_id = row[0] if row else None

    # Generate AI summary
    ai_summary = await generate_summary(body.model_dump())

    interaction = Interaction(
        hcp_id=hcp_id,
        rep_id=body.rep_id,
        interaction_type=body.interaction_type,
        interaction_date=body.interaction_date,
        interaction_time=body.interaction_time,
        attendees=json.dumps(body.attendees or []),
        topics_discussed=body.topics_discussed,
        materials_shared=json.dumps(body.materials_shared or []),
        samples_distributed=json.dumps(body.samples_distributed or []),
        sentiment=body.sentiment,
        outcomes=body.outcomes,
        follow_up_actions=body.follow_up_actions,
        ai_summary=ai_summary,
        raw_chat_input=body.raw_chat_input,
    )
    session.add(interaction)
    await session.commit()
    await session.refresh(interaction)
    return interaction


@router.get("/{interaction_id}")
async def get_interaction(interaction_id: int, session: AsyncSession = Depends(get_session)):
    interaction = await session.get(Interaction, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.put("/{interaction_id}")
async def update_interaction(
    interaction_id: int,
    body: InteractionUpdate,
    session: AsyncSession = Depends(get_session)
):
    interaction = await session.get(Interaction, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        if isinstance(value, list):
            value = json.dumps(value)
        setattr(interaction, field, value)

    await session.commit()
    await session.refresh(interaction)
    return interaction


@router.delete("/{interaction_id}")
async def delete_interaction(interaction_id: int, session: AsyncSession = Depends(get_session)):
    interaction = await session.get(Interaction, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    await session.delete(interaction)
    await session.commit()
    return {"status": "deleted", "id": interaction_id}


@router.get("/{interaction_id}/history")
async def get_hcp_interaction_history(
    interaction_id: int,
    session: AsyncSession = Depends(get_session)
):
    interaction = await session.get(Interaction, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    result = await session.execute(
        text("""
            SELECT id, interaction_type, interaction_date, topics_discussed, sentiment, ai_summary
            FROM interactions WHERE hcp_id = :hcp_id
            ORDER BY interaction_date DESC LIMIT 10
        """),
        {"hcp_id": interaction.hcp_id}
    )
    return [dict(r._mapping) for r in result.fetchall()]
