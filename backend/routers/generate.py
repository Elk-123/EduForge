from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from services.dify_service import DifyWorkflowClient
import time
import os
import httpx
import shutil
from typing import Optional

router = APIRouter()
dify_client = DifyWorkflowClient()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 1. 纯文本请求模型 (用于 JSON)
class GenerateRequest(BaseModel):
    subject: str
    stage: str = "outline"
    refined_outline: str = ""
    mode: str = "dify"

# ==================== 1. PPT 相关接口 ====================

# 【原有接口】处理纯文字 JSON 请求
@router.post("/generate-content")
async def generate_content(req: GenerateRequest):
    session_id = str(int(time.time()))
    result = await dify_client.get_eduforge_content(
        subject=req.subject, 
        stage=req.stage, 
        refined_outline=req.refined_outline
    )
    return await _handle_ppt_render(result, req.stage, session_id)

# 【新增接口】处理带 PDF/图片 的文件上传
@router.post("/generate-content-with-file")
async def generate_content_with_file(
    subject: str = Form(...),
    stage: str = Form("outline"),
    refined_outline: str = Form(""),
    file: UploadFile = File(...)
):
    session_id = str(int(time.time()))
    local_path = await _save_temp_file(file, session_id)
    
    try:
        result = await dify_client.get_eduforge_content(
            subject=subject,
            stage=stage,
            refined_outline=refined_outline,
            file_path=local_path
        )
        return await _handle_ppt_render(result, stage, session_id)
    finally:
        _cleanup_file(local_path)

# ==================== 2. 教案相关接口 ====================

# 【原有接口】处理纯文字 JSON 请求
@router.post("/generate-lesson-plan")
async def generate_lesson_plan(req: GenerateRequest):
    session_id = str(int(time.time()))
    result = await dify_client.get_eduforge_content(
        subject=req.subject,
        stage="lesson_plan",
        refined_outline=req.refined_outline
    )
    return await _handle_lesson_download(result, session_id)

# 【新增接口】处理带 PDF 的教案生成
@router.post("/generate-lesson-plan-with-file")
async def generate_lesson_plan_with_file(
    subject: str = Form(...),
    refined_outline: str = Form(""),
    file: UploadFile = File(...)
):
    session_id = str(int(time.time()))
    local_path = await _save_temp_file(file, session_id)
    
    try:
        result = await dify_client.get_eduforge_content(
            subject=subject,
            stage="lesson_plan",
            refined_outline=refined_outline,
            file_path=local_path
        )
        return await _handle_lesson_download(result, session_id)
    finally:
        _cleanup_file(local_path)

# ==================== 3. 内部公共逻辑抽离 ====================
async def _save_temp_file(file: UploadFile, session_id: str) -> str:
    path = os.path.join(UPLOAD_DIR, f"input_{session_id}_{file.filename}")
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 🌟 必须加这行！否则 Dify 读到的是空文件
    await file.seek(0) 
    return path
def _cleanup_file(path: str):
    """通用清理文件逻辑"""
    if path and os.path.exists(path):
        os.remove(path)

async def _handle_ppt_render(result: dict, stage: str, session_id: str):
    """统一处理 PPT 渲染逻辑"""
    if result.get('dsl') and stage == "generate":
        output_path = os.path.join(UPLOAD_DIR, f"output_{session_id}.pptx")
        from services.ppt_renderer import PPTRenderer
        PPTRenderer().render(result['dsl'], output_path)
        return {**result, "session_id": session_id, "download_url": f"/api/download/{session_id}"}
    return {**result, "session_id": session_id}

async def _handle_lesson_download(result: dict, session_id: str):
    """统一处理教案中转下载逻辑"""
    dify_signed_url = result.get("file_url")
    if dify_signed_url:
        try:
            local_path = os.path.join(UPLOAD_DIR, f"lesson_{session_id}.docx")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(dify_signed_url)
                if response.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(response.content)
                    return {**result, "session_id": session_id, "download_url": f"/api/download-lesson/{session_id}"}
        except Exception as e:
            print(f"中转下载失败: {e}")
    return {**result, "session_id": session_id}