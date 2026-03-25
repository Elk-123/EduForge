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
    stage: str = "generate"
    mode: str = "dify"

# ==================== 1. PPT 相关接口 ====================

# 【原有接口】处理纯文字 JSON 请求
# ==================== 升级后的统一生成接口 ====================

@router.post("/generate-content")
async def generate_content(req: GenerateRequest):
    session_id = str(int(time.time()))
    try:
        # 1. 调用 Dify 合并生成服务 (使用我们之前定义的 get_eduforge_combined_content)
        # 如果你还没改名，可以继续调用 get_eduforge_content 并确保 Dify 那边返回了两个字段
        result = await dify_client.get_eduforge_combined_content(
            subject=req.subject,
            user_id="eduforge_user"
        )
        
        # 2. 准备基础返回载体 (继承原有格式)
        response_payload = {
            "stage": req.stage,
            "ppt_content": result.get("ppt_dsl"),     # PPT 的 JSON 
            "lesson_content": result.get("lesson_text"), # 教案预览文本
            "session_id": session_id,
            "ppt_download": None,
            "lesson_download": None
        }

        # 3. 【PPT 逻辑】渲染并保存到 temp_uploads
        if result.get("ppt_dsl"):
            ppt_filename = f"ppt_{session_id}.pptx"
            ppt_path = os.path.join(UPLOAD_DIR, ppt_filename)
            
            from services.ppt_renderer import PPTRenderer
            # 执行渲染并物理保存文件
            PPTRenderer().render(result["ppt_dsl"], ppt_path)
            
            # 记录 PPT 下载地址
            response_payload["ppt_download"] = f"/api/download/{ppt_filename}"

        # 4. 【教案逻辑】从中转下载 Word 并保存到 temp_uploads
        if result.get("file_url"):
            word_filename = f"lesson_{session_id}.docx"
            word_path = os.path.join(UPLOAD_DIR, word_filename)
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                dify_res = await client.get(result["file_url"])
                if dify_res.status_code == 200:
                    with open(word_path, "wb") as f:
                        f.write(dify_res.content)
                    
                    # 记录 Word 下载地址
                    response_payload["lesson_download"] = f"/api/download/{word_filename}"

        # 返回合并后的完整对象
        return response_payload

    except Exception as e:
        print(f"❌ 接口合并执行失败: {str(e)}")
        # 即使失败也尽量保证不崩，返回 500
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")
@router.post("/generate-content-with-file")
async def generate_content_with_file(
    subject: str = Form(...),
    stage: str = Form("generate"),
    file: UploadFile = File(...)
):
    session_id = str(int(time.time()))
    local_path = await _save_temp_file(file, session_id)
    
    try:
        result = await dify_client.get_eduforge_content(
            subject=subject,
            stage=stage,
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
    )
    return await _handle_lesson_download(result, session_id)

# 【新增接口】处理带 PDF 的教案生成
@router.post("/generate-lesson-plan-with-file")
async def generate_lesson_plan_with_file(
    subject: str = Form(...),
    file: UploadFile = File(...)
):
    session_id = str(int(time.time()))
    local_path = await _save_temp_file(file, session_id)
    
    try:
        result = await dify_client.get_eduforge_content(
            subject=subject,
            stage="lesson_plan",
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