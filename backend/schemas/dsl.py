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