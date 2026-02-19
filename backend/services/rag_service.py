import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PDFIngestor:
    def parse(self, filepath):
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def chunk_text(self, text):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return splitter.split_text(text)

    # TODO: 连接 DeepSeek API 获取 Embedding 并存入 PGVector