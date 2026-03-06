# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import shutil
import os
from typing import Optional

from services.rag_service import rag_service
from services.agent_core import AgentCore
from services.ppt_renderer import PPTRenderer # 你原来的 PPT 渲染引擎
from services.session_manager import session_mgr
from schemas.dsl import PPTDocument, ChatRequest, ChatResponse

app = FastAPI(title="EduForge API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

agent = AgentCore()

# ==================== Gamma 核心交互接口 ====================

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...), 
    session_id: Optional[str] = Form(None)
):
    """前端上传文件，后端进行 RAG 向量化入库"""
    sid, state = session_mgr.get_or_create(session_id)
    
    file_path = os.path.join(UPLOAD_DIR, f"{sid}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 1. RAG 切片、向量化入库，获取简单摘要
        summary = rag_service.ingest_pdf(file_path, sid)
        
        # 2. 保存入 session
        state.file_content = summary 
        state.status = "idle"
        session_mgr.update(sid, state)
        
        return {"status": "success", "session_id": sid, "message": "文件已解析并建立知识库"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, background_tasks: BackgroundTasks):
    """右侧聊天接口，触发检索与生成"""
    sid, state = session_mgr.get_or_create(req.session_id)
    
    # 状态：告诉前端正在处理
    state.status = "processing"
    session_mgr.update(sid, state)

    # 交给图处理
    # 修改后
    response_dict = agent.process_chat(req.message, sid, state.model_dump())
    
    # 更新会话状态记录
    state.history = response_dict['history']
    state.outline = response_dict['outline']
    state.intent_complete = response_dict['is_complete']
    
    if response_dict['is_complete'] and response_dict['dsl']:
        # 🌟 关键：将 DSL 存入状态字典，供前端左侧拉取渲染
        state.current_dsl = response_dict['dsl']
        state.status = "generating_ppt"
        
        # 异步：后台渲染真实的 .pptx 物理文件
        dsl_data = PPTDocument(**response_dict['dsl'])
        background_tasks.add_task(generate_ppt_background, dsl_data, sid)
    else:
        # 如果还要继续聊天
        state.status = "waiting_user"
        
    session_mgr.update(sid, state)
    
    return ChatResponse(
        message=response_dict['message'],
        is_complete=response_dict['is_complete'],
        session_id=sid
    )

# 🌟 新增接口：供前端左侧预览区轮询获取最新数据
@app.get("/api/session/{session_id}/ppt-data")
async def get_ppt_data(session_id: str):
    """前端轮询此接口，获取最新生成的 PPT DSL JSON 渲染视图"""
    _, state = session_mgr.get_or_create(session_id)
    return {
        "status": state.status,      # 前端根据这个显示骨架屏或内容：idle, processing, generating_ppt, done
        "dsl": state.current_dsl     # 纯 JSON，前端拿着去 v-for 渲染方块页面
    }

# ==================== 后台与下载 ====================

async def generate_ppt_background(dsl_data: PPTDocument, sid: str):
    """后台任务：使用 python-pptx 渲染真实的物理文件"""
    print(f"🎨 [后台] 开始为会话 {sid} 渲染物理 PPTX...")
    renderer = PPTRenderer()
    output_filename = f"output_{sid}.pptx"
    output_path = os.path.join(UPLOAD_DIR, output_filename)
    
    try:
        renderer.render(dsl_data, output_path)
        print(f"✅ 物理 PPTX 生成成功: {output_path}")
        
        # 渲染完物理文件后，状态置为 done
        _, state = session_mgr.get_or_create(sid)
        state.status = "done"
        session_mgr.update(sid, state)
        
    except Exception as e:
        print(f"❌ 物理PPTX生成失败: {e}")

@app.get("/api/download/{session_id}")
async def download_file(session_id: str):
    """前端点击下载实体 PPTX"""
    filename = f"output_{session_id}.pptx"
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PPT文件尚未生成完毕")
        
    return FileResponse(
        file_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)