# backend/schemas/dsl.py
# backend/schemas/dsl.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union

# ==================== 页面内容模型 ====================

class PageContent(BaseModel):
    """页面内容"""
    title: str
    subtitle: Optional[str] = None
    items: Optional[List[str]] = None
    left_title: Optional[str] = None
    left_items: Optional[List[str]] = None
    right_title: Optional[str] = None
    right_items: Optional[List[str]] = None
    col1_title: Optional[str] = None
    col1_items: Optional[List[str]] = None
    col2_title: Optional[str] = None
    col2_items: Optional[List[str]] = None
    col3_title: Optional[str] = None
    col3_items: Optional[List[str]] = None
    col4_title: Optional[str] = None
    col4_items: Optional[List[str]] = None
    table_data: Optional[List[List[str]]] = None
    point1: Optional[str] = None
    point2: Optional[str] = None
    point3: Optional[str] = None
    content: Optional[str] = None

class Page(BaseModel):
    """页面模型 - 匹配 AI 的输出格式"""
    page_type: str  # 保持为 page_type，不是 type
    content: PageContent
    notes: Optional[str] = ""

class PPTDocument(BaseModel):
    """完整的PPT文档"""
    theme: str = "modern"
    background: Optional[Dict[str, Any]] = None
    pages: List[Page]

# ==================== 原有的消息和状态模型 ====================

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

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    is_complete: bool
    session_id: str