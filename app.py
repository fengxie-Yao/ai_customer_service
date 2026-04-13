# app.py

from fastapi import FastAPI
from chains.extraction import extraction_chain
from chains.intent import intent_chain
from chains.refund import handle_refund
import json

app = FastAPI()


@app.post("/chat")
async def chat(user_input: str):
    # 1. 提取信息
    extraction = extraction_chain.invoke({"text": user_input})
    extraction_data = json.loads(extraction.content)

    # 2. 判断意图
    intent = intent_chain.invoke({"text": user_input})
    intent_data = json.loads(intent.content)

    # 3. 路由
    if intent_data["intent"] == "refund":
        result = handle_refund(extraction_data)
    else:
        result = "客服处理中"

    return {
        "intent": intent_data["intent"],
        **extraction_data,
        "result": result
    }