# backend/main.py (改进版：添加/chat路由，支持多轮；/generate异步触发渲染)
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import shutil
import os
# 导入模块
from services.rag_service import PDFIngestor
from services.agent_core import AgentCore
from services.ppt_renderer import PPTRenderer
from services.session_manager import session_mgr  # 新增
from typing import TypedDict, List, Dict, Any, Optional
from schemas.dsl import PPTDocument, ChatState, ChatResponse, Message

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

class GenerateRequest(BaseModel):
    file_path: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

agent = AgentCore()  # 实例

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 提取文本 (可选立即注入session，但这里留给chat)
    return {"status": "success", "file_path": file_path}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, background_tasks: BackgroundTasks):
    sid, state = session_mgr.get_or_create(req.session_id)
    
    # 如果state无file_content，可在首次上传后注入 (假设前端上传后发chat with file_path，但这里简化)
    # 实际：可添加file_path到ChatRequest，前端上传后发chat注入
    if not state.file_content and hasattr(req, 'file_path'):  # 假设扩展
        ingestor = PDFIngestor()
        state.file_content = ingestor.extract_text(req.file_path)
    
    response_dict = agent.process_chat(req.message, state.dict())  # 用dict兼容TypedDict
    
    if response_dict['is_complete'] and response_dict['dsl']:
        dsl_data = PPTDocument(**response_dict['dsl'])  # 转Pydantic
        background_tasks.add_task(generate_ppt_background, dsl_data, sid)
    
    session_mgr.update(sid, ChatState(**state))  # 更新
    
    return ChatResponse(
        message=response_dict['message'],
        is_complete=response_dict['is_complete'],
        session_id=sid
    )

async def generate_ppt_background(dsl_data: PPTDocument, sid: str):
    print("🎨 后台渲染PPT...")
    renderer = PPTRenderer()
    output_filename = f"output_{sid}.pptx"
    output_path = os.path.join(UPLOAD_DIR, output_filename)
    renderer.render(dsl_data, output_path)
    print(f"✅ PPT生成成功: {output_path}")
    # 可SSE推送，但模块四再加

# 原有 /generate 路由（完整版，兼容单轮路径）
@app.post("/api/generate")
async def generate_ppt(req: GenerateRequest):
    print(f"\n========== 🚀 新任务启动 ==========")
    print(f"📁 1. 正在解析 PDF 教案: {req.file_path}")
    
    ingestor = PDFIngestor()
    text = ingestor.extract_text(req.file_path)
    print(f"   -> 成功提取文本: 共 {len(text)} 个字符")
    
    print("🧠 2. 正在呼叫 DeepSeek (LangGraph 工作流) 思考中...")
    agent = AgentCore()
    dsl_data = agent.generate_ppt_dsl(text)   # 注意这里用 generate_ppt_dsl
    
    print("🎨 3. 正在将 AI 数据交给渲染引擎生成 PPT...")
    renderer = PPTRenderer()
    
    # 【关键修复】在这里明确定义 output_filename
    base_name = os.path.splitext(os.path.basename(req.file_path))[0]
    output_filename = f"output_{base_name}.pptx"   # 或用 sid，如果有会话
    output_path = os.path.join(UPLOAD_DIR, output_filename)
    
    renderer.render(dsl_data, output_path)
    
    print(f"✅ 4. 生成成功！文件保存至: {output_path}\n===================================")
    return {"status": "success", "download_url": f"/api/download/{output_filename}"}

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    return FileResponse(
        file_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)