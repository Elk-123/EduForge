# backend/schemas/dsl.py (改进版：添加对话相关模型，不改原有PPTDocument)
from pydantic import BaseModel, Field
from typing import List, Optional

class SlideContent(BaseModel):
    title: str = Field(description="幻灯片的主标题")
    subtitle: Optional[str] = Field(None, description="副标题，仅在封面页使用")
    items: Optional[List[str]] = Field(None, description="正文内容要点列表，每句话尽量简短")

class SlidePage(BaseModel):
    page_type: str = Field(description="页面类型，只能是 'title' (封面) 或 'content' (正文内容)")
    content: SlideContent = Field(description="幻灯片具体内容")
    notes: Optional[str] = Field(None, description="教师演讲时的逐字稿备注")

class PPTDocument(BaseModel):
    theme: str = Field(description="课件主题风格，如 'modern', 'classic'")
    pages: List[SlidePage] = Field(description="幻灯片页面列表")

# 新增：对话模型
class Message(BaseModel):
    role: str = Field(..., description="user or assistant")
    content: str = Field(..., description="消息内容")

class ChatState(BaseModel):
    history: List[Message] = Field(default_factory=list, description="对话历史")
    file_content: str = Field("", description="上传文件提取的文本")  # 继承原有file_content
    intent_complete: bool = False  # 是否意图完整
    dsl_output: Optional[dict] = None  # 生成的DSL dict (原有格式)

class ChatResponse(BaseModel):
    message: str  # AI回复
    is_complete: bool
    session_id: Optional[str] = None  # 返回给前端会话ID