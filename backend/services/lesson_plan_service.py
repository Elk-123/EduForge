# backend/services/lesson_plan_service.py
import os
import re
from .dify_service import DifyWorkflowClient
from .lesson_renderer import LessonRenderer

class LessonPlanService:
    def __init__(self):
        # 1. 正常实例化，此时它内部拿的是环境变量里的 DIFY_API_KEY (PPT用的)
        self.dify_client = DifyWorkflowClient()
        
        # 2. 🌟 手动覆盖属性：强行将 Key 替换为教案专用 Key
        lesson_key = os.getenv("DIFY_API_KEY_LESSON")
        if lesson_key:
            self.dify_client.api_key = lesson_key
        
        self.renderer = LessonRenderer()

    async def stream_lesson_plan(self, subject: str):
        """调用教案专用的 Dify 工作流"""
        # 这里的 stage 对应 Dify 截图中的分支逻辑
        async for chunk in self.dify_client.stream_eduforge_workflow(
            subject=subject,
            stage="lesson_plan" 
        ):
            yield chunk

    def parse_markdown_to_data(self, markdown_content: str) -> dict:
        """解析教案 Markdown 表格，对应 docxtpl 的变量"""
        data = {
            "title": "未命名教案",
            "steps": []
        }
        
        # 提取标题
        title_match = re.search(r"^#\s+(.*)", markdown_content, re.M)
        if title_match:
            data["title"] = title_match.group(1).strip()

        # 解析 Markdown 表格行
        table_rows = re.findall(r"\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|", markdown_content)
        if len(table_rows) > 2: 
            for row in table_rows[2:]: # 过滤表头和分割线
                data["steps"].append({
                    "phase": row[0].strip(),
                    "time": row[1].strip(),
                    "teacher_act": row[2].strip(),
                    "student_act": row[3].strip()
                })
        return data