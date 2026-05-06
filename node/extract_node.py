from chains.extraction import extraction_chain
from utils.parser import call_with_retry, validate_extraction
from utils.state import AgentState


def extract_node(state: AgentState):
    extraction_data = call_with_retry(
        extraction_chain,
        {"text": state["messages"][-1].content},
        {"order_id": "", "product": "", "issue": ""},
        validate_extraction
    )
    print(extraction_data)
    return {
        "order_id": extraction_data.get("order_id") or state["order_id"],
        "product": extraction_data.get("product") or state["product"],
        "issue": extraction_data.get("issue") or state["issue"],
    }
