from rag.chain import rag_answer
from utils.state import AgentState
from langchain_core.messages import AIMessage

def refund_node(state: AgentState):
    return {"messages": [AIMessage(content="已进入退款流程")]}


def rag_node(state: AgentState):
    answer = rag_answer(
        state["messages"][-1].content,
        state["messages"],
        {
            "order_id": state["order_id"],
            "product": state["product"],
            "issue": state["issue"],
            "intent": state["intent"]
        }
    )
    return {"messages": [AIMessage(content=answer)]}
