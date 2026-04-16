from langchain_community.embeddings import DashScopeEmbeddings
import os

# 设置 API Key
# os.environ["DASHSCOPE_API_KEY"] = "your-dashscope-api-key"

# 初始化嵌入模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",  # 或其他支持的模型，如 text-embedding-v2
)

# 正确传入字符串或字符串列表
texts = ["你好世界", "这是一个测试"]
embeddings_result = embeddings.embed_documents(texts)

# 单个文本
single_embedding = embeddings.embed_query("你好")
print(single_embedding)