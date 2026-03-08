# backend/services/dify_service.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class DifyWorkflowClient:
    def __init__(self):
        self.api_key = os.getenv("DIFY_API_KEY")
        self.base_url = "https://api.dify.ai/v1/workflows/run"

    async def run_eduforge_workflow(self, subject: str, user_id: str = "eduforge_user"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": {"subject": subject},
            "response_mode": "blocking",
            "user": user_id
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()