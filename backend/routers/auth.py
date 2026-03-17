# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, User
from schemas.auth import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class AuthSchema(BaseModel):
    username: str
    email: str
    password: str

@router.post("/register")
def register(data: AuthSchema, db: Session = Depends(get_db)):
    # 检查重名
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="用户名已被注册")
    
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="该邮箱已被注册")
    # 使用我们的新原生哈希函数
    new_user = User(
        username=data.username, 
        email=data.email,
        hashed_password=get_password_hash(data.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "注册成功"}

@router.post("/login")
def login(
    data: OAuth2PasswordRequestForm = Depends(), # 🌟 关键修改：改用这个
    db: Session = Depends(get_db)
):
    # 这里的 data 会自动包含 .username 和 .password
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="账号或密码错误")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}