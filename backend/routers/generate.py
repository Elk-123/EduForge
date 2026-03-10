from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel  # 🌟 新增导入 BaseModel
from services.dify_service import DifyWorkflowClient

router = APIRouter()
dify_client = DifyWorkflowClient()

# 🌟 1. 定义一个 Pydantic 模型来接收 JSON 请求体
class GenerateRequest(BaseModel):
    subject: str
    task_type: str = "outline"
    refined_outline: str = ""
    mode: str = "dify"

# 🌟 2. 将路由参数改为接收刚才定义的模型
@router.post("/generate-content")
async def generate_content(req: GenerateRequest):
    if req.mode == "dify":
        # 注意：这里改成了使用 req.subject, req.task_type 等
        return StreamingResponse(
            dify_client.stream_eduforge_workflow(
                subject=req.subject, 
                task_type=req.task_type, 
                refined_outline=req.refined_outline
            ),
            media_type="text/plain"
        )
    else:
        return {"source": "langgraph", "data": "original_logic_output"}