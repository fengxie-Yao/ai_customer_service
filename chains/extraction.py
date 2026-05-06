# chains/extraction.py
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from utils.prompt import load_prompt

llm = ChatOpenAI(
    model='qwen3-32b',
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    extra_body={
        "enable_thinking": False  # 开启思考
    }
)

prompt = ChatPromptTemplate.from_template(
    load_prompt("prompts/extraction.txt")
)

extraction_chain = prompt | llm