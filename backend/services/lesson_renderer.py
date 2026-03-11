# backend/services/lesson_renderer.py
from docxtpl import DocxTemplate
import os
from typing import Dict, Any

class LessonRenderer:
    def __init__(self, template_path: str = "templates/lesson_plan_template.docx"):
        # 确保你有一个预设好的 Word 模板
        self.template_path = template_path

    def render(self, data: Dict[str, Any], output_path: str):
        """
        data 包含：title, objectives, teaching_process, homework 等
        """
        if not os.path.exists(self.template_path):
            # 如果没有模板，这里可以写一个基础的逻辑生成简单 docx，
            # 但建议大赛演示一定要用精美的模板。
            from docx import Document
            doc = Document()
            doc.add_heading(data.get('title', 'Lesson Plan'), 0)
            doc.add_paragraph(data.get('content', ''))
            doc.save(output_path)
            return

        doc = DocxTemplate(self.template_path)
        # 将数据渲染进模板
        doc.render(data)
        doc.save(output_path)