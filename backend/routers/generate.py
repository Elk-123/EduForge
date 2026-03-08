# backend/routers/generate.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse  # 【新增导入】
from services.dify_service import DifyWorkflowClient
# from services.agent_core import AgentCore 

router = APIRouter()
dify_client = DifyWorkflowClient()

@router.post("/generate-content")
async def generate_content(
    subject: str, 
    task_type: str = "outline", 
    refined_outline: str = "", 
    mode: str = "dify"
):
    if mode == "dify":
        # 【关键修改】返回 StreamingResponse，并将 Content-Type 设置为 text/plain 
        # 这样前端就能像打字机一样一段段接收到纯文本
        return StreamingResponse(
            dify_client.stream_eduforge_workflow(
                subject=subject, 
                task_type=task_type, 
                refined_outline=refined_outline
            ),
            media_type="text/plain"
        )
    else:
        # 你原来的 LangGraph 逻辑（假设这里目前仍然是阻塞式，以后也可改成流式）
        # result = await LangGraphAgent.run(subject)
        return {"source": "langgraph", "data": "original_logic_output"}