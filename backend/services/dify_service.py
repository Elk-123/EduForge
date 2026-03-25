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
    async def get_eduforge_combined_content(
        self, subject: str, file_path: str = None, user_id: str = "eduforge_user"
    ):
        # 统一使用 PPT 的 API KEY（假设你的 Dify 工作流在一个应用里同时处理这两者）
        headers = {"Authorization": f"Bearer {self.ppt_api_key}", "Content-Type": "application/json"}

        inputs = {
            "subject": str(subject or "未命名主题"),
            "stage": "combined_generate", # 告诉 Dify 同时生成两者
        }

        payload = {
            "inputs": inputs,
            "query": subject,
            "response_mode": "blocking",
            "user": user_id
        }

        # 处理文件上传（逻辑保持不变）
        if file_path and os.path.exists(file_path):
            file_id = await self._upload_file(file_path, self.ppt_api_key)
            ext = os.path.splitext(file_path)[1].lower()
            file_type = "image" if ext in [".png", ".jpg", ".jpeg"] else "document"
            payload["files"] = [{"type": file_type, "transfer_method": "local_file", "upload_file_id": file_id}]

        # 增加 ReadTimeout 容错
        timeout = httpx.Timeout(300.0, connect=60.0, read=None)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{self.base_url}/chat-messages", headers=headers, json=payload)
            response.raise_for_status()
            resp_data = response.json()

        # --- 核心合并解析逻辑 ---
        outputs = resp_data.get("data", {}).get("outputs", {})
        raw_answer = resp_data.get("answer", "")

        # 1. 提取教案链接 (如果有)
        dify_file_url = None
        file_match = re.search(r'\[.*?\.docx\]\((.*?)\)', raw_answer)
        if file_match:
            dify_file_url = file_match.group(1)
            if dify_file_url.startswith('/'):
                dify_file_url = f"http://127.0.0.1{dify_file_url}"

        # 2. 提取 PPT DSL
        # 兼容多种可能的输出变量名
        ppt_dsl = outputs.get("ppt_dsl") or outputs.get("dsl") or outputs.get("ppt_content")
        # 3. 提取纯文本教案 (用于前端 A4 纸即时预览)
        lesson_text = outputs.get("lesson_plan") or outputs.get("text_content") or raw_answer
        if not ppt_dsl:
            # 匹配从第一个 { 到最后一个 } 的所有内容
            # re.DOTALL 让 . 匹配包括换行符在内的所有字符
            json_match = re.search(r'(\{.*\})', lesson_text, re.DOTALL)
            if json_match:
                ppt_dsl_candidate = json_match.group(1).strip()
                try:
                    # 验证提取的是否为合法 JSON
                    json.loads(ppt_dsl_candidate)
                    ppt_dsl = ppt_dsl_candidate
                except json.JSONDecodeError:
                    ppt_dsl = None
        print("------------------------------------")
        if ppt_dsl:
            try:
                # 🌟 关键：将字符串转为字典对象
                ppt_dsl= json.loads(ppt_dsl)
            except json.JSONDecodeError:
                ppt_dsl = None
                print("❌ JSON 格式错误，无法解析")
        print(ppt_dsl)
        return {
            "ppt_dsl": ppt_dsl,
            "lesson_text": lesson_text,
            "file_url": dify_file_url,
            "message": "课件与教案生成完毕"
        }