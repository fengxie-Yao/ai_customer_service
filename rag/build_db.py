import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# 读取数据
with open("../data/faq.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 切分
splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=100,
    chunk_overlap=20,
    length_function=len
)
texts = splitter.split_text(text)
texts = [t.strip() for t in texts if t.strip()]

# embedding
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
)

# 构建向量库
db = FAISS.from_texts(texts, embeddings)

# 保存
db.save_local("../data/vector_store")