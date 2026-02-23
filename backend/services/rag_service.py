# backend/services/rag_service.py
import fitz  # PyMuPDF
import os

class PDFIngestor:
    def extract_text(self, filepath: str) -> str:
        """从 PDF 中提取纯文本"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"❌ 文件未找到: {filepath}")
        
        try:
            doc = fitz.open(filepath)
            text = ""
            # 为了 MVP 阶段不让 AI 等太久，我们先限制读取前 5 页
            for page_num in range(min(5, doc.page_count)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            print(f"❌ PDF 解析失败: {str(e)}")
            raise e