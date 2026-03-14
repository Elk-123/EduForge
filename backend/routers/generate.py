from fastapi import APIRouter
# from fastapi.responses import StreamingResponse  # 🌟 移除，不再需要流式响应
from pydantic import BaseModel
from services.dify_service import DifyWorkflowClient
from services.lesson_plan_service import LessonPlanService

router = APIRouter()
dify_client = DifyWorkflowClient()
lp_service = LessonPlanService()

class GenerateRequest(BaseModel):
    subject: str
    stage: str = "outline"
    refined_outline: str = ""
    mode: str = "dify"

@router.post("/generate-content")
async def generate_content(req: GenerateRequest):
    if req.mode == "dify":
        # 🌟 修改点：直接等待完整结果返回，不再使用 StreamingResponse
        result = await dify_client.get_eduforge_content(
            subject=req.subject, 
            stage=req.stage, 
            refined_outline=req.refined_outline
        )
        return result
    else:
        return {"source": "langgraph", "data": "original_logic_output"}

class LessonPlanRequest(BaseModel):
    subject: str
    stage: str = "lesson_plan"
    user_id: str = "eduforge_user"

@router.post("/generate-lesson-plan")
async def generate_lesson_plan(req: LessonPlanRequest):
    # 🌟 修改点：改为调用 lp_service 的同步/完整传输接口 (假设已在 service 中实现 get_lesson_plan)
    result = await lp_service.get_lesson_plan(req.subject)
    return result