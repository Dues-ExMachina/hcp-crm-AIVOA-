from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from groq import AsyncGroq
from core.config import settings

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def get_hcp_history_tool(hcp_name: str, session: AsyncSession, limit: int = 5) -> dict:
    """
    Tool 3: Retrieves last N interactions for a given HCP by name.
    Uses LLM to clean up the name if it's buried in a conversational sentence.
    """
    search_name = hcp_name
    if len(hcp_name.split()) > 3:
        try:
            prompt = f"Extract ONLY the doctor's name (e.g., 'Dr. Sharma') from this sentence: '{hcp_name}'. Return nothing else."
            response = await client.chat.completions.create(
                model=settings.GROQ_MODEL_PRIMARY,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            extracted = response.choices[0].message.content.strip()
            if extracted and len(extracted) < 30:
                search_name = extracted
        except Exception as e:
            print(f"Name extraction failed: {e}")

    # Remove generic titles if LLM returned them generically
    search_name = search_name.replace("Dr. ", "").replace("Dr ", "")

    result = await session.execute(
        text("""
            SELECT i.id, i.interaction_type, i.interaction_date, i.topics_discussed,
                   i.sentiment, i.outcomes, i.ai_summary, h.name as hcp_full_name
            FROM interactions i
            JOIN hcps h ON i.hcp_id = h.id
            WHERE h.name LIKE :name
            ORDER BY i.interaction_date DESC
            LIMIT :limit
        """),
        {"name": f"%{search_name}%", "limit": limit}
    )
    rows = result.fetchall()
    history = [dict(r._mapping) for r in rows]

    return {"hcp_name": search_name, "history": history, "count": len(history)}
