from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings

embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
)

# db = FAISS.load_local("vector_store", embeddings)

db = FAISS.load_local(
    "data/vector_store",
    embeddings,
    allow_dangerous_deserialization=True  # 加上这行！
)

retriever = db.as_retriever(search_kwargs={"k": 2})
