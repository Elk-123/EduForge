from fastapi import File, UploadFile, APIRouter
import shutil
import os

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 触发后台解析任务 (这里先模拟)
    return {"filename": file.filename, "status": "uploaded", "path": file_path}