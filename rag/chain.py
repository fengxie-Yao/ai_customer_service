import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from rag.retriever import retriever
from unils.prompt import load_prompt

llm = ChatOpenAI(
    model='qwen3-32b',
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    extra_body={
        "enable_thinking": False  # 开启思考
    }
)

def rag_answer(question: str):
    docs = retriever.invoke(question)
    context = "\n".join([d.page_content for d in docs])

    prompt = ChatPromptTemplate.from_template(
        load_prompt("prompts/rag.txt")
    )

    chain = prompt | llm

    result = chain.invoke({
        "context": context,
        "question": question
    })

    return result.content