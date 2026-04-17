import json
from datetime import date
from groq import AsyncGroq
from core.config import settings
from agent.state import AgentState

# Use Async client for FastAPI
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# ── Node 1: Intent Classifier ──────────────────────────────────────────────────
async def intent_classifier_node(state: AgentState) -> AgentState:
    """
    Uses llama-3.3-70b-versatile to classify the user's intent asynchronously.
    """
    print(f"\n--- CLASSIFYING INTENT ---")
    print(f"Message: {state['user_input']}")

    system_prompt = """You are a specialized pharma CRM assistant. Identify the user's intent. 
Intents:
- log: User is describing a interaction/meeting/call they just had.
- edit: User wants to change something already logged.
- history: User asks about past interactions (e.g., "When did I last see...")
- search: User wants to find an HCP (e.g., "Search for Dr. Smith")
- followup: User asks for suggestions.

Return ONLY JSON: {"intent": "log" | "edit" | "history" | "search" | "followup" | "unknown"}"""

    try:
        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL_PRIMARY,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": state["user_input"]}
            ],
            max_tokens=50,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw.strip())
        intent = data.get("intent", "unknown")
        print(f"Detected Intent: {intent}")
        
    except Exception as e:
        print(f"Classification Error: {e}")
        intent = "unknown"
        return {**state, "tool_to_call": intent, "error": str(e)}

    return {**state, "tool_to_call": intent}


# ── Node 2: Interaction Data Extractor ────────────────────────────────────────
async def extract_interaction_node(state: AgentState) -> AgentState:
    """
    Uses llama-3.3-70b-versatile to extract all structured fields asynchronously.
    """
    today = date.today().isoformat()
    intent = state.get("tool_to_call", "log")
    chat_lines = [f"{msg.get('role')}: {msg.get('content')}" for msg in state.get("chat_history", [])]
    chat_context = "\n".join(chat_lines[-4:]) if chat_lines else "None"

    prompt = f"""You are a data extraction assistant for a pharmaceutical field CRM.
Today's date is {today}.

Context from previous messages:
{chat_context}

Extract interaction details from this field rep message and return ONLY valid JSON.
If the message is asking to UPDATE or EDIT something, ONLY return the fields specifically mentioned to be changed! Keep everything else null!

Message: "{state['user_input']}"

JSON schema (use null for missing fields):
{{
  "hcp_name": "string or null",
  "interaction_type": "Meeting or Call or Email or Conference or null",
  "interaction_date": "YYYY-MM-DD or null",
  "interaction_time": "HH:MM or null",
  "attendees": ["string array or null"],
  "topics_discussed": "string or null",
  "materials_shared": ["string array or null"],
  "samples_distributed": ["string array or null"],
  "sentiment": "Positive or Neutral or Negative or null",
  "outcomes": "string or null",
  "follow_up_actions": "string or null"
}}"""

    try:
        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL_CONTEXT,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        raw = response.choices[0].message.content.strip()
        extracted = json.loads(raw)
    except Exception as e:
        print(f"Extraction Error: {e}")
        extracted = {}
        return {**state, "error": f"Extraction failed: {str(e)}"}

    # Fill defaults only if it's a new log
    if intent == "log" and not extracted.get("interaction_date"):
        extracted["interaction_date"] = today

    return {**state, **extracted}


# ── Node 3: Follow-up Suggester ────────────────────────────────────────────────
async def suggest_followups_node(state: AgentState) -> AgentState:
    """
    Uses llama-3.3-70b-versatile to suggest next steps asynchronously.
    """
    chat_lines = [f"{msg.get('role')}: {msg.get('content')}" for msg in state.get("chat_history", [])]
    chat_context = "\n".join(chat_lines[-4:]) if chat_lines else "None"

    prompt = f"""You are a pharmaceutical sales coach.
Based on this HCP interaction history and context, suggest exactly 3 specific, actionable follow-up items.
Return ONLY JSON: ["suggestion 1", "suggestion 2", "suggestion 3"]

Interaction context:
- HCP: {state.get('hcp_name') or 'Unknown'}
- Topics: {state.get('topics_discussed') or 'N/A'}
- Sentiment: {state.get('sentiment') or 'Neutral'}

Recent Chat History:
{chat_context}"""

    try:
        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL_PRIMARY,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw.strip())
        
        if isinstance(data, list):
            suggestions = data
        elif isinstance(data, dict):
            suggestions = next((v for v in data.values() if isinstance(v, list)), [])
        else:
            suggestions = []
            
    except Exception as e:
        print(f"Suggestion Error: {e}")
        suggestions = [
            "Schedule a follow-up meeting within 2 weeks",
            "Send relevant clinical study materials",
            "Update CRM with outcome and next steps",
        ]

    return {**state, "suggested_followups": suggestions}


# ── Node 4: Response Formatter ─────────────────────────────────────────────────
def response_formatter_node(state: AgentState) -> AgentState:
    """
    Formats a friendly reply message to the rep.
    """
    tool = state.get("tool_to_call", "unknown")
    error = state.get("error")

    if error and tool == "unknown":
        reply = "I'm sorry, I couldn't understand your request. Please try again with more details, for example: 'Met Dr. Sharma today, discussed OncoBoost, positive sentiment.'"
    elif tool == "log":
        hcp = state.get("hcp_name") or "the HCP"
        reply = (
            f"✅ Got it! I've extracted the interaction details for {hcp}. "
            f"The form has been populated — please review, make any edits, and click **Save Interaction**."
        )
    elif tool == "edit":
        result = state.get("tool_result") or {}
        fields = result.get("updated_fields", [])
        reply = f"✅ Interaction updated successfully. Fields changed: {', '.join(fields) if fields else 'none'}."
    elif tool == "history":
        result = state.get("tool_result") or {}
        history = result.get("history", [])
        if history:
            lines = [f"• **{h.get('interaction_date')}** — {h.get('topics_discussed', 'No topics logged')}" for h in history[:5]]
            reply = f"📋 Here are the recent interactions:\n" + "\n".join(lines)
        else:
            reply = "No past interactions found for that HCP."
    elif tool == "search":
        result = state.get("tool_result") or {}
        hcps = result.get("results", [])
        if hcps:
            lines = [f"• {h['name']} ({h.get('specialty', 'N/A')}) — {h.get('territory', 'N/A')}" for h in hcps[:5]]
            reply = "🔍 HCPs found:\n" + "\n".join(lines)
        else:
            reply = "No HCPs found matching your search."
    elif tool == "followup":
        suggestions = state.get("suggested_followups", [])
        if suggestions:
            lines = [f"{i+1}. {s}" for i, s in enumerate(suggestions)]
            reply = "💡 Suggested follow-up actions:\n" + "\n".join(lines)
        else:
            reply = "I couldn't generate follow-up suggestions at this time."
    else:
        reply = "I'm here to help you log HCP interactions. Try saying something like: 'Met Dr. Patel today at 3pm, discussed Product X, shared brochure, positive sentiment.'"

    return {**state, "reply": reply}


# ── Node 5: Error Handler ──────────────────────────────────────────────────────
def error_handler_node(state: AgentState) -> AgentState:
    reply = f"⚠️ An error occurred: {state.get('error', 'Unknown error')}. Please try again."
    return {**state, "reply": reply}
