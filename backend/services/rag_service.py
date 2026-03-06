# backend/services/rag_service.py
import os
from dotenv import load_dotenv  # 🌟 新增：导入 dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 🌟 新增：确保在此文件加载时，读取 .env 文件中的环境变量
load_dotenv()

class RAGService:
    def __init__(self):
        # 🌟 新增：获取 key 并增加防御性检查
        api_key = os.getenv("SILICONFLOW_API_KEY")
        if not api_key:
            raise ValueError("❌ 启动失败：未找到 SILICONFLOW_API_KEY，请检查项目根目录下是否有 .env 文件且配置正确！")

        # 使用 SiliconFlow 提供的向量模型 (如 BAAI/bge-m3 免费且支持多语言)
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base="https://api.siliconflow.cn/v1",
            model="BAAI/bge-m3" 
        )
        self.vector_stores = {} # 内存缓存 vector store, key 为 session_id

    # ... 下面的 ingest_pdf 和 retrieve_context 方法保持不变 ...

    def ingest_pdf(self, filepath: str, session_id: str) -> str:
        """解析 PDF、切片并存入向量库"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"❌ 文件未找到: {filepath}")
        
        print(f"📚 [RAG] 开始进行知识入库: {filepath}")
        # 1. 加载文档
        loader = PyMuPDFLoader(filepath)
        documents = loader.load()
        
        # 2. 文本切分 (Chunking)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,   # 每块800字符
            chunk_overlap=150,# 重叠150字符保证上下文
            separators=["\n\n", "\n", "。", "！", "？", " ", ""]
        )
        splits = text_splitter.split_documents(documents)
        
        if not splits:
            return "文件内容为空或无法提取。"
            
        # 3. 向量化并建立索引
        vector_store = FAISS.from_documents(splits, self.embeddings)
        self.vector_stores[session_id] = vector_store
        
        print(f"✅ [RAG] 入库完成，共分为 {len(splits)} 块。Session: {session_id}")
        
        # 4. 返回前1000字作为初始摘要，给 Agent 基础判断用
        summary = "\n".join([doc.page_content for doc in splits[:2]])
        return summary[:1000]

    def retrieve_context(self, session_id: str, query: str, k: int = 4) -> str:
        """根据用户问题/意图，检索最相关的 K 个教材片段"""
        if session_id not in self.vector_stores:
            return ""
        
        print(f"🔍 [RAG] 正在检索教材内容，Query: {query[:20]}...")
        vector_store = self.vector_stores[session_id]
        docs = vector_store.similarity_search(query, k=k)
        
        context = "\n---\n".join([doc.page_content for doc in docs])
        return context

# 全局单例
rag_service = RAGService()