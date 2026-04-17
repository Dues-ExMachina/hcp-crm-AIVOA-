from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import (
    intent_classifier_node,
    extract_interaction_node,
    suggest_followups_node,
    response_formatter_node,
    error_handler_node,
)


def route_by_intent(state: AgentState) -> str:
    """Conditional edge: routes after intent classification."""
    intent = state.get("tool_to_call", "unknown")
    if intent in ("log", "edit", "history", "search", "followup"):
        return intent
    return "unknown"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # ── Nodes ──────────────────────────────────────────────────────────────────
    graph.add_node("classify_intent",     intent_classifier_node)
    graph.add_node("extract_interaction", extract_interaction_node)
    graph.add_node("suggest_followups",   suggest_followups_node)
    graph.add_node("format_response",     response_formatter_node)

    # ── Entry point ────────────────────────────────────────────────────────────
    graph.set_entry_point("classify_intent")

    # ── Conditional routing after classification ───────────────────────────────
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "log":      "extract_interaction",
            "edit":     "extract_interaction",
            "history":  "extract_interaction",
            "search":   "format_response",
            "followup": "extract_interaction",
            "unknown":  "format_response",
        }
    )

    # ── Linear edges ───────────────────────────────────────────────────────────
    graph.add_edge("extract_interaction", "suggest_followups")
    graph.add_edge("suggest_followups",   "format_response")
    graph.add_edge("format_response",     END)

    return graph.compile()


# Build singleton graph
crm_graph = build_graph()
