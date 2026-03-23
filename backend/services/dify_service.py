import httpx
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

class DifyWorkflowClient:
    def __init__(self):
        self.ppt_api_key = os.getenv("DIFY_API_KEY")
        self.lesson_api_key = os.getenv("DIFY_API_KEY_LESSON")
        self.base_url = "http://127.0.0.1/v1"

    # --- 第一步：上传文件到 Dify 获取 file_id ---
    async def _upload_file(self, file_path: str, api_key: str):
        url = f"{self.base_url}/files/upload"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # 自动识别文件类型
        ext = os.path.splitext(file_path)[1].lower()
        mime_type = "application/pdf" if ext == ".pdf" else "image/jpeg"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, mime_type)}
                response = await client.post(url, headers=headers, files=files)
                response.raise_for_status()
                return response.json().get("id")

    # --- 第二步：发送消息并关联文件 ---
    async def get_eduforge_content(
        self, subject: str, stage: str = "outline", 
        refined_outline: str = "", file_path: str = None, user_id: str = "eduforge_user"
    ):
        current_key = self.lesson_api_key if stage == "lesson_plan" else self.ppt_api_key
        headers = {"Authorization": f"Bearer {current_key}", "Content-Type": "application/json"}

        # 🌟 核心修复：无论什么 stage，都保证这三个核心变量不为 None 且都存在
        safe_subject = str(subject or "未命名主题")
        safe_stage = str(stage or "outline")
        safe_outline = str(refined_outline or "")
        # backend/services/dify_service.py
        inputs = {
            "subject": safe_subject,
            "stage": safe_stage,
            "text": safe_subject,     # 👈 很多默认节点会找这个变量
            "query": safe_subject,    # 👈 兼容对话型应用
        }

        payload = {
            "inputs": inputs,
            "query": safe_subject,    # 👈 确保 query 字段不为空
            "response_mode": "blocking",
            "user": user_id
        }

        # 处理文件类型
        if file_path and os.path.exists(file_path):
            file_id = await self._upload_file(file_path, current_key)
            ext = os.path.splitext(file_path)[1].lower()

            # 🌟 核心点：确保如果是图片，type 必须是 image
            file_type = "image" if ext in [".png", ".jpg", ".jpeg"] else "document"
            payload["files"] = [{
                "type": file_type,
                "transfer_method": "local_file",
                "upload_file_id": file_id
            }]
        timeout = httpx.Timeout(120.0, connect=60.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{self.base_url}/chat-messages", headers=headers, json=payload)
            if response.status_code == 400:
                print(f"❌ Dify 400 Error Detail: {response.text}")
            response.raise_for_status()
            resp_data = response.json()

        # --- 解析逻辑 ---
        outputs = resp_data.get("data", {}).get("outputs", {})
        raw_answer = resp_data.get("answer", "")
        
        # 提取 Word 下载链接（针对教案插件）
        dify_file_url = None
        file_match = re.search(r'\[.*?\.docx\]\((.*?)\)', raw_answer)
        if file_match:
            dify_file_url = file_match.group(1)
            if dify_file_url.startswith('/'):
                dify_file_url = f"http://127.0.0.1{dify_file_url}"
        
        clean_markdown = re.sub(r'\[.*?\.docx\]\(.*?\)\n?', '', raw_answer).strip()

        # 处理 DSL (PPT 或教案文本)
        final_dsl = clean_markdown if stage == "lesson_plan" else (
            outputs.get("ppt_outline") or outputs.get("ppt_content") or outputs.get("dsl")
        )

        return {
            "stage": stage,
            "message": outputs.get("text_reply", "生成成功"),
            "dsl": final_dsl,
            "file_url": dify_file_url,
            "is_complete": True if final_dsl or dify_file_url else False,
            "raw_response": resp_data 
        }