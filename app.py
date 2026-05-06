# app.py
import sentry_sdk
from fastapi import FastAPI
from graph.chat_graph import graph
from langchain_core.messages import HumanMessage, AIMessage
from utils.redis_client import RedisSessionStore

redis_session_store = RedisSessionStore()

sentry_sdk.init(
    dsn="https://79520b895f8acbe8a13692b13765be0c@o4511341561511936.ingest.us.sentry.io/4511341564264448",
    send_default_pii=True,
)

app = FastAPI()


@app.post("/chat")
async def chat(user_input: str, session_id: str):
    new_user_message = HumanMessage(content=user_input)
    session = redis_session_store.get(session_id)
    result = graph.invoke({
        "messages": session['memory'] + [new_user_message],
        "order_id": session["state"]["order_id"],
        "product": session["state"]["product"],
        "issue": session["state"]["issue"],
        "intent": session["state"]["intent"]
    })
    STATE_KEYS = ("order_id", "product", "issue", "intent")
    for key in STATE_KEYS:
        value = result.get(key)  # 不存在时返回 None，不抛 KeyError
        if value:
            session["state"][key] = value

    # for key in session['state']:
    #     if result[key]:
    #         session['state'][key] = result[key]

    session["memory"] = result["messages"]
    redis_session_store.save(session_id, session)
    return {
        "result": result,
    }
