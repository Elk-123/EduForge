import httpx
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

class DifyWorkflowClient:
    def __init__(self):
        self.api_key = os.getenv("DIFY_API_KEY")
        self.base_url = "https://api.dify.ai/v1/chat-messages"

    # 🌟 修改点：方法名改为 get_eduforge_content，移除 yield，改为 return
    async def get_eduforge_content(
        self, subject: str, stage: str = "outline", refined_outline: str = "", user_id: str = "eduforge_user"
    ):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "inputs": {"subject": subject, "stage": stage, "refined_outline": refined_outline},
            "query": f"开始生成{subject}的{stage}",
            "response_mode": "blocking", # 🌟 修改点：由 streaming 改为 blocking
            "user": user_id
        }
        
        timeout = httpx.Timeout(120.0, connect=60.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            # 🌟 修改点：直接发送 POST 请求并解析完整的 JSON
            response = await client.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            resp_data = response.json()
        # --- 原 process_chat 的解析逻辑开始 ---
        
        # 1. 提取输出字段 (兼容不同工作流配置)
        outputs = resp_data.get("metadata", {}) or resp_data.get("data", {}).get("outputs", {})
        
        # 优先从 outputs 取 ppt_content，如果没有则尝试解析 answer 里的 JSON
        final_dsl = outputs.get("ppt_content")
        raw_answer = resp_data.get("answer", "")
        
        # 如果 outputs 里没拿到，就从 answer 字符串里正则抠 JSON
        if not final_dsl and raw_answer:
            try:
                if "```json" in raw_answer:
                    json_str = re.search(r'```json\s*(.*?)\s*```', raw_answer, re.DOTALL).group(1)
                elif "```" in raw_answer:
                    json_str = re.search(r'```\s*(.*?)\s*```', raw_answer, re.DOTALL).group(1)
                else:
                    json_str = raw_answer
                final_dsl = json.loads(json_str.strip())
            except Exception:
                final_dsl = None

        # 2. 提取文本回复内容
        clean_message = outputs.get("text_reply", raw_answer if not final_dsl else "PPT 数据已准备就绪")

        # --- 终端打印调试 ---
        print(f"\n🚀 [Dify Output] Stage: {stage}")
        print(f"📝 Message: {clean_message[:50]}...")
        print(f"📊 DSL Generated: {'Yes' if final_dsl else 'No'}")

        # 返回统一的业务对象
        return {
            "message": clean_message,
            "dsl": final_dsl,
            "is_complete": True if final_dsl else False,
            "raw_response": resp_data  # 保留原始响应以备不时之需
        }
