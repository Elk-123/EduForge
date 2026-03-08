from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
import shutil
import os
from typing import Optional

# 1. 导入你已经创建好的数据库和认证模块
from database import engine, Base
from routers import auth, generate  # 🌟 1. 导入 generate 路由

from services.rag_service import rag_service
from services.agent_core import AgentCore
from services.ppt_renderer import PPTRenderer 
from services.session_manager import session_mgr
from schemas.dsl import PPTDocument, ChatRequest, ChatResponse

# 自动创建数据库表（如果 users 表不存在会在此步创建）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduForge API")

# 定义 OAuth2 方案，指向你的登录接口，方便在 Swagger UI (/docs) 测试
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

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

# 挂载认证路由 (包含 /api/auth/register 和 /api/auth/login)
app.include_router(auth.router, prefix="/api/auth") # 建议统一前缀
app.include_router(generate.router, prefix="/api/v1") # 🌟 2. 挂载生成路由

# ==================== Gamma 核心交互接口 ====================

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...), 
    session_id: Optional[str] = Form(None),
    token: str = Depends(oauth2_scheme) # 🌟 必须登录才能上传
):
    """前端上传文件，后端进行 RAG 向量化入库"""
    sid, state = session_mgr.get_or_create(session_id)
    
    file_path = os.path.join(UPLOAD_DIR, f"{sid}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 1. RAG 切片、向量化入库
        summary = rag_service.ingest_pdf(file_path, sid)
        
        # 2. 保存入 session
        state.file_content = summary 
        state.status = "idle"
        session_mgr.update(sid, state)
        
        return {"status": "success", "session_id": sid, "message": "文件已解析并建立知识库"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    req: ChatRequest, 
    background_tasks: BackgroundTasks,
    token: str = Depends(oauth2_scheme) # 🌟 必须登录才能对话
):
    """右侧聊天接口，触发检索与生成"""
    sid, state = session_mgr.get_or_create(req.session_id)
    
    state.status = "processing"
    session_mgr.update(sid, state)

    # 交给 Agent 处理
    response_dict = agent.process_chat(req.message, sid, state.model_dump())
    
    state.history = response_dict['history']
    state.outline = response_dict['outline']
    state.intent_complete = response_dict['is_complete']
    
    if response_dict['is_complete'] and response_dict['dsl']:
        state.current_dsl = response_dict['dsl']
        state.status = "generating_ppt"
        
        dsl_data = PPTDocument(**response_dict['dsl'])
        background_tasks.add_task(generate_ppt_background, dsl_data, sid)
    else:
        state.status = "waiting_user"
        
    session_mgr.update(sid, state)
    
    return ChatResponse(
        message=response_dict['message'],
        is_complete=response_dict['is_complete'],
        session_id=sid
    )

@app.get("/api/session/{session_id}/ppt-data")
async def get_ppt_data(session_id: str, token: str = Depends(oauth2_scheme)):
    """前端轮询此接口，获取最新生成的 PPT DSL JSON"""
    _, state = session_mgr.get_or_create(session_id)
    return {
        "status": state.status,
        "dsl": state.current_dsl
    }

# ==================== 后台与下载 ====================

async def generate_ppt_background(dsl_data: PPTDocument, sid: str):
    """后台任务：使用 python-pptx 渲染真实的物理文件"""
    renderer = PPTRenderer()
    output_filename = f"output_{sid}.pptx"
    output_path = os.path.join(UPLOAD_DIR, output_filename)
    
    try:
        renderer.render(dsl_data, output_path)
        _, state = session_mgr.get_or_create(sid)
        state.status = "done"
        session_mgr.update(sid, state)
    except Exception as e:
        print(f"❌ 物理PPTX生成失败: {e}")

@app.get("/api/download/{session_id}")
async def download_file(session_id: str, token: str = Depends(oauth2_scheme)):
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