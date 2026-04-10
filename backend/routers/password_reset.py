# backend/routers/password_reset.py
import random
import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional # 记得在文件顶部导入 Optional

# 导入你现有的数据库和密码工具
from database import get_db, User
from schemas.auth import get_password_hash

router = APIRouter(prefix="/api", tags=["Password Reset"])

# ==================== 配置区 ====================
# 1. 邮件服务器配置 (⚠️ 强烈建议将其移至 .env 文件中)
conf = ConnectionConfig(
    MAIL_USERNAME="19975020159@163.com",      # 发件邮箱
    MAIL_PASSWORD="PMX2Zu95Dehwvxke",           # 注意：是 SMTP 授权码，不是登录密码！
    MAIL_FROM="19975020159@163.com",          # 发件人
    MAIL_PORT=465,                        # QQ/网易邮箱通常是 465
    MAIL_SERVER="smtp.163.com",            # SMTP 服务器地址
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)

# 2. 模拟 Redis 存储验证码 (开发测试用，格式: {"user@email.com": {"code": "123456", "expire": 169...}})
fake_redis_db = {}

# 3. 找回密码专用的临时 Token 秘钥
RESET_SECRET_KEY = "eduforge_reset_secret_key_123!"
ALGORITHM = "HS256"


# ==================== Pydantic 数据模型 ====================
class SendCodeSchema(BaseModel):
    email: EmailStr
    captcha: Optional[str] = None         # 前端的图形验证码
    captchaKey: Optional[str] = None     # 前端的图形验证码ID

class VerifyCodeSchema(BaseModel):
    email: EmailStr
    code: str

class ResetPasswordSchema(BaseModel):
    email: EmailStr
    password: str
    confirmPassword: str
    token: str           # 验证邮箱后获取的临时通行证


# ==================== 接口 1: 发送邮箱验证码 ====================
@router.post("/send-email-code")
async def send_email_code(data: SendCodeSchema, db: Session = Depends(get_db)):
    # 1. 检查该邮箱是否在我们的数据库中注册过
    # user = db.query(User).filter(User.email == data.email).first()
    # if not user:
        # raise HTTPException(status_code=404, detail="该邮箱未注册")

    # 2. (可选) 这里应该校验图形验证码 data.captcha 是否正确，防机器人刷邮件
    # if data.captcha != "正确的图形验证码":
    #     raise HTTPException(status_code=400, detail="图形验证码错误")

    # 3. 生成 6 位随机验证码
    verification_code = str(random.randint(100000, 999999))

    # 4. 存入 "Redis" (5分钟有效期)
    fake_redis_db[data.email] = {
        "code": verification_code,
        "expire_at": time.time() + 300 
    }

    # 5. 发送邮件
    html_content = f"""
    <div style="padding: 20px; background-color: #f9f9f9;">
        <h2>EduForge 密码重置验证</h2>
        <p>您的验证码是：<strong style="color: #4CAF50; font-size: 24px;">{verification_code}</strong></p>
        <p>该验证码将在 5 分钟后失效。请勿泄露给他人。</p>
    </div>
    """
    message = MessageSchema(
        subject="【EduForge】密码重置验证码",
        recipients=[data.email],
        body=html_content,
        subtype=MessageType.html
    )

    try:
        fm = FastMail(conf)
        await fm.send_message(message)
        return {"success": True, "message": "验证码已发送", "data": {"expireIn": 300}}
    except Exception as e:
        print(f"邮件发送失败: {e}")
        raise HTTPException(status_code=500, detail="邮件发送失败，请检查服务器配置")


# ==================== 接口 2: 验证邮箱验证码 ====================
@router.post("/verify-email-code")
async def verify_email_code(data: VerifyCodeSchema):
    record = fake_redis_db.get(data.email)

    if not record:
        raise HTTPException(status_code=400, detail="请先获取验证码")

    if time.time() > record["expire_at"]:
        del fake_redis_db[data.email]
        raise HTTPException(status_code=400, detail="验证码已过期，请重新获取")

    if record["code"] != data.code:
        raise HTTPException(status_code=400, detail="验证码错误")

    # 验证成功，销毁验证码
    del fake_redis_db[data.email]

    # 【核心安全设计】颁发一个专门用于重置密码的临时 Token (15分钟有效)
    expire = datetime.utcnow() + timedelta(minutes=15)
    # payload 中加入 "type": "reset" 防止和登录用的 Token 混淆
    payload = {"sub": data.email, "type": "reset", "exp": expire}
    reset_token = jwt.encode(payload, RESET_SECRET_KEY, algorithm=ALGORITHM)

    return {
        "success": True, 
        "message": "验证成功",
        "data": {"token": reset_token} # 对应前端的 data.data.token
    }


# ==================== 接口 3: 提交新密码 ====================
@router.post("/reset-password")
async def reset_password(data: ResetPasswordSchema, db: Session = Depends(get_db)):
    # 1. 基础校验
    if data.password != data.confirmPassword:
        raise HTTPException(status_code=400, detail="两次输入的密码不一致")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="密码长度不能少于6位")

    # 2. 校验 Token 的合法性
    try:
        payload = jwt.decode(data.token, RESET_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if email != data.email or token_type != "reset":
            raise HTTPException(status_code=401, detail="非法或失效的操作凭证")
    except JWTError:
        raise HTTPException(status_code=401, detail="验证信息已过期，请重新开始流程")

    # 3. 查找用户
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 4. 更新密码（必须要哈希加密！）
    user.hashed_password = get_password_hash(data.password)
    db.commit() # 提交到数据库

    return {"success": True, "message": "密码重置成功"}