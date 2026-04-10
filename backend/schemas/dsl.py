# backend/schemas/dsl.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PageContent(BaseModel):
    title: str
    subtitle: Optional[str] = None
    items: Optional[List[str]] = None

class Page(BaseModel):
    page_type: str
    content: PageContent
    notes: Optional[str] = ""

class PPTDocument(BaseModel):
    theme: str = "modern"
    pages: List[Page]

class Message(BaseModel):
    role: str
    content: str

class ChatState(BaseModel):
    history: List[Dict[str, str]] = []
    file_content: str = ""       
    outline: str = ""
    intent_complete: bool = False
    
    # UI 状态同步
    status: str = "idle"         
    current_dsl: Optional[Dict[str, Any]] = None 

# 🌟 新增：把前端请求的模型也统一放在这里
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    is_complete: bool
    session_id: str