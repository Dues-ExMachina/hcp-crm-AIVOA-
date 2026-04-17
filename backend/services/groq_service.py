from groq import Groq
from core.config import settings

_client = None

def get_groq_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


async def generate_summary(data: dict) -> str:
    """
    Uses gemma2-9b-it to generate a concise AI summary of an interaction.
    """
    client = get_groq_client()
    prompt = f"""
You are a pharmaceutical CRM assistant. Write a concise 2-3 sentence summary of this HCP interaction for a field rep's records.

Details:
- HCP: {data.get('hcp_name') or 'Unknown'}
- Type: {data.get('interaction_type') or 'Meeting'}
- Date: {data.get('interaction_date') or 'Today'}
- Topics: {data.get('topics_discussed') or 'N/A'}
- Materials Shared: {data.get('materials_shared') or 'None'}
- Samples: {data.get('samples_distributed') or 'None'}
- Sentiment: {data.get('sentiment') or 'Neutral'}
- Outcomes: {data.get('outcomes') or 'None noted'}
- Follow-up: {data.get('follow_up_actions') or 'None'}

Write a professional, factual summary paragraph only. No bullet points.
"""
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL_PRIMARY,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()
