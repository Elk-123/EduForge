# backend/services/rag_service.py (微改：添加set_file_content方法，便于会话注入文件文本)
import fitz  # PyMuPDF
import os

class PDFIngestor:
    def extract_text(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"❌ 文件未找到: {filepath}")
        
        try:
            doc = fitz.open(filepath)
            text = ""
            for page_num in range(min(5, doc.page_count)):  # 保持原有限制，后续模块三升级
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            print(f"❌ PDF 解析失败: {str(e)}")
            raise e