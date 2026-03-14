from fastapi import APIRouter
# from fastapi.responses import StreamingResponse  # 🌟 移除，不再需要流式响应
from pydantic import BaseModel
from services.dify_service import DifyWorkflowClient
from services.lesson_plan_service import LessonPlanService
import time
import os
from services.ppt_renderer import PPTRenderer   # 假设你有一个 ppt_renderer 模块负责 PPT 渲染
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
    session_id =str(int(time.time())) # 生成一个唯一的 session_id，确保每次请求都不同
    download_url = None
    if req.mode == "dify":
        # 🌟 修改点：直接等待完整结果返回，不再使用 StreamingResponse
        result = await dify_client.get_eduforge_content(
            subject=req.subject, 
            stage=req.stage, 
            refined_outline=req.refined_outline
        )
        if result.get('dsl'):
            UPLOAD_DIR = "temp_uploads"
            output_filename =f"output_{session_id}.pptx"
            output_path = os.path.join(UPLOAD_DIR, output_filename)
            ppt_renderer = PPTRenderer()
            ppt_renderer.render(result['dsl'], output_path)
            download_url = f"/api/download/{session_id}"
            print(f"PPT渲染完成，下载链接: {download_url}.{output_path}")
            return{
                **result,
                "session_id": session_id,
                "download_url": download_url
            }
        else:
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