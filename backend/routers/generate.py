from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from services.dify_service import DifyWorkflowClient
import time
import os
import httpx
import shutil
from typing import Optional
import json

router = APIRouter()
dify_client = DifyWorkflowClient()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
class UpdateRequest(BaseModel):
    message: str           # 用户输入的修改指令
    session_id: str        # 必传：用来找 JSON 文件的钥匙
    active_tab: str        # 'ppt' 或 'lesson'
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
        if result.get("ppt_dsl"):
            json_filename = f"data_{session_id}.json"
            json_path = os.path.join(UPLOAD_DIR, json_filename)
            import json
            with open(json_path, "w", encoding="utf-8") as f:
                # 这里的 ppt_dsl 已经是字典对象了，直接 dump
                json.dump(result["ppt_dsl"], f, ensure_ascii=False, indent=4)
            print(f"💾 已持久化原始 JSON: {json_path}")
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
        print(f"✅ 接口合并执行成功: {response_payload}")
        return response_payload

    except Exception as e:
        print(f"❌ 接口合并执行失败: {str(e)}")
        # 即使失败也尽量保证不崩，返回 500
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")
@router.post("/update-content")
async def update_content(req: UpdateRequest):
    import json # 🌟 强制在函数内部导入，防止全局没导
    import traceback
    
    print(f"🚀 [DEBUG] 收到修改请求: session_id={req.session_id}, tab={req.active_tab}")
    
    try:
        json_path = os.path.join(UPLOAD_DIR, f"data_{req.session_id}.json")
        print(f"📂 [DEBUG] 检查文件是否存在: {json_path}")
        
        if not os.path.exists(json_path):
            print("❌ [DEBUG] 文件不存在！")
            raise HTTPException(status_code=404, detail="找不到原始课件记录")

        with open(json_path, "r", encoding="utf-8") as f:
            old_ppt_dsl = json.load(f)
        print("✅ [DEBUG] 成功读取旧 JSON")

        # 构造参数
        current_stage = "changeword" if req.active_tab == "lesson" else "changeppt"
        # 🌟 检查这一步是否崩了
        try:
            refined_subject = f"修改要求：{req.message}"
            old_content_str = json.dumps(old_ppt_dsl, ensure_ascii=False)
        except Exception as json_err:
            print(f"❌ [DEBUG] JSON 序列化失败: {json_err}")
            raise

        print(f"📡 [DEBUG] 正在尝试连接 Dify...")
        print (current_stage)
        # 真正发送请求
        result = await dify_client.get_eduforge_combined_content(
            subject=refined_subject,
            old_content=old_content_str,
            stage=current_stage,
            user_id="eduforge_user"
        )
        print("🎉 [DEBUG] Dify 响应成功！")
        return {"status": "success", "data": result}

    except Exception as e:
        print("🔥 [CRITICAL] 接口彻底崩了，以下是详细报错信息：")
        traceback.print_exc() # 👈 这行代码会在黑窗口打印具体的报错行号
        raise HTTPException(status_code=500, detail=str(e))