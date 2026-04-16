# app.py

from fastapi import FastAPI
from chains.extraction import extraction_chain
from chains.intent import intent_chain
from chains.refund import handle_refund
from chains.chat import chat_chain
from unils.parser import validate_extraction, validate_intent, call_with_retry, safe_json_parse
from unils.prompt import format_history
from rag.chain import rag_answer

app = FastAPI()

session_store = {

}
@app.post("/chat")
async def chat(user_input: str, session_id: str):
    # 会话记忆
    session = session_store.get(session_id, {
        "memory": [],
        'state':{
            "order_id": "",
            "product": "",
            "issue": ""
        }
    })
    session["memory"].append({
        "role": "user",
        "content": user_input
    })
    # 提取信息
    extraction_data = call_with_retry(
        extraction_chain,
        {"text": user_input},
        {"order_id": "", "product": "", "issue": ""},
        validate_extraction
    )
    # 更新 session（关键）
    for key in session['state']:
        if extraction_data[key]:
            session['state'][key] = extraction_data[key]

    session_store[session_id] = session

    # 判断意图
    intent_data = call_with_retry(
        intent_chain,
        {"text": user_input},
        {"intent": "query"},
        validate_intent
    )
    # 客服回复
    history = format_history(session["memory"])
    chat_response = chat_chain.invoke(
        {
            "state": session["state"],
            "history": history,
            "input": user_input
        }
    )
    # print(chat_response.content)
    chat_response = safe_json_parse(chat_response.content, "请输入您的问题")

    # 路由
    if intent_data["intent"] == "refund":
        result = handle_refund(extraction_data)
    elif intent_data["intent"] == "complaint":
        result = "请输入您的投诉内容"
    elif intent_data["intent"] == "query":
        result = rag_answer(user_input)
    else:
        result = "客服处理中"

    return {
        "session_id":session_id,
        "intent": intent_data["intent"],
        **session['state'],
        "result": result,
        "response":chat_response['response']
    }