from langgraph.graph import StateGraph

from node.decision_node import router
from node.intent_node import intent_node
from node.extract_node import extract_node
from node.untility_node import rag_node, refund_node
from utils.state import AgentState

builder = StateGraph(AgentState)

builder.add_node("extract", extract_node)
builder.add_node("intent", intent_node)
builder.add_node("refund", refund_node)
builder.add_node("rag", rag_node)

builder.set_entry_point("extract")

builder.add_edge("extract", "intent")

builder.add_conditional_edges(
    "intent",
    router,
    {
        "refund": "refund",
        "rag": "rag"
    }
)

graph = builder.compile()