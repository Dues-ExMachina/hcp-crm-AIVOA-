from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def get_interaction_by_id(interaction_id: int, session: AsyncSession):
    result = await session.execute(
        text("SELECT * FROM interactions WHERE id = :id"),
        {"id": interaction_id}
    )
    row = result.fetchone()
    return dict(row._mapping) if row else None


async def get_last_interaction_for_rep(rep_id: int, session: AsyncSession):
    result = await session.execute(
        text("SELECT * FROM interactions WHERE rep_id = :rep_id ORDER BY created_at DESC LIMIT 1"),
        {"rep_id": rep_id}
    )
    row = result.fetchone()
    return dict(row._mapping) if row else None
