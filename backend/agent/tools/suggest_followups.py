import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from groq import Groq
from core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


async def suggest_followups_tool(hcp_id: int, current_context: str, session: AsyncSession) -> dict:
    """
    Tool 4: Generates AI-powered follow-up recommendations using Groq.
    Pulls last 3 interactions for context using gemma2-9b-it.
    """
    # Fetch last 3 interactions for this HCP
    result = await session.execute(
        text("""
            SELECT topics_discussed, outcomes, sentiment, ai_summary
            FROM interactions
            WHERE hcp_id = :hcp_id
            ORDER BY interaction_date DESC
            LIMIT 3
        """),
        {"hcp_id": hcp_id}
    )
    past = [dict(r._mapping) for r in result.fetchall()]

    prompt = f"""You are a pharmaceutical sales coach. Based on this HCP's interaction history
and the current visit context, suggest 3-5 specific, actionable follow-up items for the field rep.
Return a JSON array of strings ONLY, no extra text.

Past interactions: {json.dumps(past)}
Current context: {current_context}"""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL_PRIMARY,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        suggestions = json.loads(raw.strip())
    except Exception:
        suggestions = [
            "Schedule follow-up meeting in 2 weeks",
            "Send requested clinical data",
            "Update CRM with today's outcomes",
        ]

    return {"suggested_followups": suggestions}
