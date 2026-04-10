# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
import shutil
import os
from typing import Optional

# 1. 导入你已经创建好的数据库和认证模块
from database import engine, Base
from routers import auth, generate, password_reset 
from services.ppt_renderer import PPTRenderer 
from schemas.dsl import PPTDocument
from services.lesson_renderer import LessonRenderer
from services.lesson_plan_service import LessonPlanService

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

# 挂载认证路由 (包含 /api/auth/register 和 /api/auth/login)
app.include_router(auth.router)
app.include_router(password_reset.router) # 🌟 1. 挂载密码重置路由
app.include_router(generate.router, prefix="/api/v1") # 🌟 2. 挂载生成路由

# ==================== Gamma 核心交互接口 ====================

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...), 
    session_id: Optional[str] = Form(None),
    token: str = Depends(oauth2_scheme) # 🌟 必须登录才能上传
):  
    # Placeholder implementation for the upload_file endpoint
    return {"status": "success", "message": "File uploaded successfully"}
    

# ==================== 后台与下载 ====================

# @app.get("/api/download/{session_id}")
# async def download_file(session_id: str):
#     """前端点击下载实体 PPTX"""
#     filename = f"output_{session_id}.pptx"
#     file_path = os.path.join(UPLOAD_DIR, filename)
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="PPT文件尚未生成完毕")
        
#     return FileResponse(
#         file_path,
#         filename=filename,
#         media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
#     )
@app.get("/api/download/{file_name}")
async def download_file(file_name: str):

    """
    通用下载接口：根据文件名从 temp_uploads 抓取文件
    file_name 会自动捕获 URL 里的字符串，如 "ppt_1775033944.pptx"
    """
    file_path = os.path.abspath(os.path.join(UPLOAD_DIR, file_name))
    
    # 在后端控制台（黑窗口）打印
    print(f"--- 调试信息 ---")
    print(f"当前程序运行目录: {os.getcwd()}")
    print(f"尝试读取的绝对路径: {file_path}")
    print(f"该路径是否存在: {os.path.exists(file_path)}")
    
    if not os.path.exists(file_path):
        # 🌟 把绝对路径直接返回给前端，让你在浏览器一眼看到错在哪
        raise HTTPException(
            status_code=404, 
            detail=f"后端在路径 [{file_path}] 找不到文件。请核对文件夹名和文件名。"
        )
    # 安全校验：防止有人用 ../../etc/passwd 偷看系统文件
    if ".." in file_name or "/" in file_name:
        raise HTTPException(status_code=400, detail="非法的文件名")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件尚未生成，请稍后再试")
        
    # 根据后缀自动设置文件类型，让浏览器知道怎么处理
    media_type = 'application/octet-stream'
    if file_name.endswith('.pptx'):
        media_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    elif file_name.endswith('.docx'):
        media_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        
    return FileResponse(
        file_path,
        filename=file_name, # 下载到用户电脑时显示的名字
        media_type=media_type
    )

lesson_renderer = LessonRenderer()

lp_service_logic = LessonPlanService()

@app.post("/api/lesson-plan/build")
async def build_lesson_doc(session_id: str, content: str, title: str):
    filename = f"lesson_{session_id}.docx"
    output_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # 🌟 关键：先解析 Markdown 表格
        parsed_data = lp_service_logic.parse_markdown_to_data(content)
        # 如果解析出了标题，覆盖传入的简单 title
        parsed_data["title"] = title or parsed_data.get("title") 
        
        # 调用渲染器
        lp_service_logic.renderer.render(parsed_data, output_path)
        return {"status": "success", "download_url": f"/api/download-lesson/{session_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)