# backend/routers/generate.py
from fastapi import APIRouter, Depends
from services.dify_service import DifyWorkflowClient
from services.agent_core import AgentCore # 假设这是你原来的逻辑

router = APIRouter()
dify_client = DifyWorkflowClient()

@router.post("/generate-content")
async def generate_content(subject: str, mode: str = "dify"):
    if mode == "dify":
        result = await dify_client.run_eduforge_workflow(subject)
        
        # 🌟 调试用：在终端打印完整的返回结构，看看到底 key 是什么
        print(f"DEBUG: Dify Response -> {result}")
        
        # 使用安全取值方式，避免 KeyError 崩溃
        data_obj = result.get("data", {})
        outputs = data_obj.get("outputs", {})
        
        # 检查 Dify 返回的是 'text' 还是其他名字（比如有的节点默认叫 'result'）
        generated_text = outputs.get("text") or outputs.get("result") or "No content generated"
        
        return {
            "source": "dify",
            "data": generated_text,
            "raw_status": data_obj.get("status")
        }
    else:
        # 使用你原来的 LangGraph 逻辑
        # result = await LangGraphAgent.run(subject)
        return {"source": "langgraph", "data": "original_logic_output"}