from chains.intent import intent_chain
from utils.parser import call_with_retry, validate_intent
from utils.state import AgentState


def intent_node(state: AgentState):
    intent_data = call_with_retry(
        intent_chain,
        {"text": state["messages"][-1].content},
        {"intent": "query"},
        validate_intent
    )

    return {"intent": intent_data.get("intent", "query")}
