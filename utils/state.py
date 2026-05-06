from typing import TypedDict, Annotated

from langgraph.graph import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    order_id: str
    product: str
    issue: str
    intent: str