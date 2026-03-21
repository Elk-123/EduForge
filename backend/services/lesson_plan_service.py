import os
import re
import uuid
from .dify_service import DifyWorkflowClient
from .lesson_renderer import LessonRenderer

class LessonPlanService:
    async def get_lesson_plan(self, subject: str):
        # 1. 调用 Dify 工作流
        result = await self.dify_client.run_workflow(subject=subject)
        
        # 2. 直接提取预览文本和插件生成的链接
        # 假设你在 Dify 结束节点定义的变量名是 answer 和 docx_file
        preview_markdown = result.get("outputs", {}).get("answer")
        dify_file_obj = result.get("outputs", {}).get("docx_file", {})
        download_url = dify_file_obj.get("url")

        return {
            "status": "success",
            "markdown": preview_markdown,   # 给前端做网页预览
            "download_url": download_url    # 给前端做文件下载
        }