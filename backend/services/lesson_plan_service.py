# backend/services/lesson_plan_service.py
import os
import re
import uuid
from .dify_service import DifyWorkflowClient
from .lesson_renderer import LessonRenderer

class LessonPlanService:
    def __init__(self):
        # 1. 初始化 Client
        self.dify_client = DifyWorkflowClient()
        
        # 2. 覆盖教案专用 Key
        lesson_key = os.getenv("DIFY_API_KEY_LESSON")
        if lesson_key:
            self.dify_client.api_key = lesson_key
        
        self.renderer = LessonRenderer()

    async def get_lesson_plan(self, subject: str):
        """
        彻底的一次性获取逻辑：
        直接调用 get_eduforge_content（非流式接口）
        """
        # --- 1. 一次性获取完整结果 ---
        # 这里的 get_eduforge_content 内部应该是 await self.post(...) 
        # 而不是 yield chunks
        result = await self.dify_client.get_eduforge_content(
            subject=subject,
            stage="lesson_plan"
        )
        
        # 假设 Dify 返回的结构中，正文在 result['answer'] 或 result['data']['outputs']['text']
        full_markdown = result.get("answer", "") or result.get("text", "")

        if not full_markdown:
            return {"status": "error", "message": "Dify 未返回任何内容"}

        # --- 2. 解析 Markdown 表格 ---
        parsed_data = self.parse_markdown_to_data(full_markdown)

        # --- 3. 渲染 Word 文档 ---
        session_id = uuid.uuid4().hex
        output_filename = f"lesson_{session_id}.docx"
        UPLOAD_DIR = "temp_uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        output_path = os.path.join(UPLOAD_DIR, output_filename)
        
        # 调用 Word 渲染器
        self.renderer.render(parsed_data, output_path)

        # --- 4. 返回完整 JSON ---
        return {
            "status": "success",
            "session_id": session_id,
            "title": parsed_data.get("title"),
            "markdown": full_markdown,
            "data": parsed_data["steps"],
            "download_url": f"/api/download/{session_id}"
        }

    def parse_markdown_to_data(self, markdown_content: str) -> dict:
        """解析教案 Markdown 表格（保持不变）"""
        data = {"title": "未命名教案", "steps": []}
        
        title_match = re.search(r"^#\s+(.*)", markdown_content, re.M)
        if title_match:
            data["title"] = title_match.group(1).strip()

        table_rows = re.findall(r"\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|", markdown_content)
        if len(table_rows) > 2: 
            for row in table_rows[2:]:
                data["steps"].append({
                    "phase": row[0].strip(),
                    "time": row[1].strip(),
                    "teacher_act": row[2].strip(),
                    "student_act": row[3].strip()
                })
        return data