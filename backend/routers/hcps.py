from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from core.database import get_session

router = APIRouter()


@router.get("/search")
async def search_hcps(q: str = "", session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        text("""
            SELECT id, name, specialty, territory, email, phone
            FROM hcps
            WHERE name LIKE :q OR specialty LIKE :q OR territory LIKE :q
            ORDER BY name
            LIMIT 20
        """),
        {"q": f"%{q}%"}
    )
    rows = result.fetchall()
    return {"results": [dict(r._mapping) for r in rows]}


@router.get("/{hcp_id}")
async def get_hcp(hcp_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        text("SELECT * FROM hcps WHERE id = :id"), {"id": hcp_id}
    )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="HCP not found")
    return dict(row._mapping)
