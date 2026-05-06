import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from rag.retriever import retriever
from utils.prompt import load_prompt

llm = ChatOpenAI(
    model='qwen3-32b',
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    extra_body={
        "enable_thinking": False  # 开启思考
    }
)

def rag_answer(question, history, state):
    # 🔥 构造增强查询（关键）
    enhanced_query = f"""
    用户当前问题：{question}
    已知信息：{state}
    历史对话：{history}
    """

    docs = retriever.invoke(enhanced_query)
    context = "\n".join([d.page_content for d in docs])
    prompt = ChatPromptTemplate.from_template(
        load_prompt("prompts/rag.txt")
    )

    chain = prompt | llm
    # print(prompt)
    result = chain.invoke({
        "context": context,
        "question": question
    })

    return result.content