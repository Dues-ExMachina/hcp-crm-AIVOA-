import json
import re
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from groq import AsyncGroq
from core.config import settings

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def search_hcp_tool(query: str, session: AsyncSession, limit: int = 10) -> dict:
    """
    Tool 5: Searches HCPs by name, specialty, or territory using precise LLM extraction and AND logic.
    """
    search_params = {"name": None, "specialty": None, "territory": None}
    
    # Use LLM to extract structured search parameters
    try:
        prompt = f"""Extract search parameters from this query: '{query}'. 
If it's a medical specialist (like 'cardiologists'), convert it to the base department name (like 'Cardiology').
Return ONLY a JSON object with keys: "name", "specialty", "territory". Use null if a parameter is not specified."""
        
        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL_PRIMARY,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
        )
        raw = response.choices[0].message.content.strip()
        
        # Try to find JSON block using regex
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            raw_json = json_match.group(0)
            extracted = json.loads(raw_json)
            search_params.update({k: v for k, v in extracted.items() if v})
        else:
            raise ValueError("No JSON object found in response")
    except Exception as e:
        print(f"Filter extraction failed: {e}")
        # Fallback to single string search if extraction completely fails
        search_params["name"] = query

    print(f"Executing DB search for params: {search_params}")
    
    # Build dynamic SQL query
    conditions = []
    sql_params = {"limit": limit}
    
    if search_params.get("name"):
        conditions.append("LOWER(name) LIKE LOWER(:name)")
        sql_params["name"] = f"%{search_params['name']}%"
    if search_params.get("specialty"):
        conditions.append("LOWER(specialty) LIKE LOWER(:specialty)")
        sql_params["specialty"] = f"%{search_params['specialty']}%"
    if search_params.get("territory"):
        conditions.append("LOWER(territory) LIKE LOWER(:territory)")
        sql_params["territory"] = f"%{search_params['territory']}%"
        
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query_str = f"""
        SELECT id, name, specialty, territory, email, phone
        FROM hcps
        WHERE {where_clause}
        ORDER BY name
        LIMIT :limit
    """
    
    result = await session.execute(text(query_str), sql_params)
    hcps = [dict(r._mapping) for r in result.fetchall()]

    return {"results": hcps, "count": len(hcps)}
