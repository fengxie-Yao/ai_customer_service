from utils.state import AgentState


def router(state: AgentState):
    if state["intent"] == "refund":
        return "refund"
    else:
        return "rag"