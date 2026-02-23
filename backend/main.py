# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import os

# 导入我们的三大核心模块
from services.rag_service import PDFIngestor
from services.agent_core import AgentCore
from services.ppt_renderer import PPTRenderer

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

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "success", "file_path": file_path}

@app.post("/api/generate")
async def generate_ppt(req: GenerateRequest):
    print(f"\n========== 🚀 新任务启动 ==========")
    print(f"📁 1. 正在解析 PDF 教案: {req.file_path}")
    ingestor = PDFIngestor()
    text = ingestor.extract_text(req.file_path)
    print(f"   -> 成功提取文本: 共 {len(text)} 个字符")
    
    print("🧠 2. 正在呼叫 DeepSeek (LangGraph 工作流) 思考中...")
    agent = AgentCore()
    dsl_data = agent.generate_ppt_dsl(text) 
    
    print("🎨 3. 正在将 AI 数据交给渲染引擎生成 PPT...")
    renderer = PPTRenderer()
    
    # 【修复重点】去除原来的后缀名 (例如 .pdf)，只加上 .pptx
    base_name = os.path.splitext(os.path.basename(req.file_path))[0]
    output_filename = f"output_{base_name}.pptx"
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