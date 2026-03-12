# backend/routers/generate.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel  # 🌟 新增导入 BaseModel
from services.dify_service import DifyWorkflowClient
from services.lesson_plan_service import LessonPlanService

router = APIRouter()
dify_client = DifyWorkflowClient()
# 专门的教案服务 (内部已处理独立 API KEY)
lp_service = LessonPlanService()

# 🌟 1. 定义一个 Pydantic 模型来接收 JSON 请求体
class GenerateRequest(BaseModel):
    subject: str
    stage: str = "outline"  # 🌟 与 Dify 保持一致
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
                stage=req.stage, # 🌟 传参对齐
                refined_outline=req.refined_outline
            ),
            media_type="text/event-stream", # 🌟 SSE 标准流式类型
            # 🌟 新增：强制禁用代理缓存
            headers={
                "X-Accel-Buffering": "no",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
    else:
        return {"source": "langgraph", "data": "original_logic_output"}
    
# backend/routers/generate.py (新增部分)

class LessonPlanRequest(BaseModel):
    subject: str
    stage: str = "lesson_plan" # 对应 Dify 里的分支判断
    user_id: str = "eduforge_user"

@router.post("/generate-lesson-plan")
async def generate_lesson_plan(req: LessonPlanRequest):
    # 🌟 这里必须改用 lp_service 提供的 stream 接口
    return StreamingResponse(
        lp_service.stream_lesson_plan(req.subject),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache"
        }
    )