# backend/services/ppt_renderer.py
from pptx import Presentation
from schemas.dsl import PPTDocument
import os

class PPTRenderer:
    def __init__(self, template_path=None):
        self.template_path = template_path

    def render(self, dsl_data, output_file: str) -> str:
        # 1. 数据兼容层：确保我们处理的是 Pydantic 对象
        if isinstance(dsl_data, dict):
            try:
                dsl_data = PPTDocument(**dsl_data)
            except Exception as e:
                print(f"⚠️ [Renderer] 数据格式转换警告: {e}")
                self._create_fallback_ppt(output_file, "AI 数据结构不匹配")
                return output_file

        # 2. 准备画布
        prs = Presentation(self.template_path) if self.template_path else Presentation()
        
        try:
            # 3. 开始渲染每一页
            for page in dsl_data.pages:
                if page.page_type == 'title':
                    slide_layout = prs.slide_layouts[0] # 0号母版通常是封面
                    slide = prs.slides.add_slide(slide_layout)
                    slide.shapes.title.text = page.content.title
                    if page.content.subtitle and len(slide.placeholders) > 1:
                        slide.placeholders[1].text = page.content.subtitle
                else:
                    slide_layout = prs.slide_layouts[1] # 1号母版通常是带标题的列表页
                    slide = prs.slides.add_slide(slide_layout)
                    slide.shapes.title.text = page.content.title
                    # 填充正文列表
                    if page.content.items and len(slide.placeholders) > 1:
                        tf = slide.placeholders[1].text_frame
                        # 写入第一行
                        tf.text = page.content.items[0] if page.content.items else ""
                        # 追加后面的行
                        for item in page.content.items[1:]:
                            p = tf.add_paragraph()
                            p.text = item
                
                # 写入演讲者备注
                if page.notes and slide.has_notes_slide:
                    slide.notes_slide.notes_text_frame.text = page.notes
                    
            # 4. 保存文件 (最关键的一步)
            prs.save(output_file)
            print(f"✅ [Renderer] PPT 渲染成功，完美保存！")
            
        except Exception as e:
            print(f"❌ [Renderer] 渲染引擎发生严重错误: {e}")
            self._create_fallback_ppt(output_file, str(e))
            
        return output_file

    def _create_fallback_ppt(self, output_file: str, error_msg: str):
        """降级方案：当渲染失败时，输出一个报错 PPT 占位，防止系统崩溃"""
        print("⚠️ [Renderer] 正在生成安全降级 PPT 文件...")
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = "引擎渲染失败"
        slide.placeholders[1].text = f"抱歉，AI 传回的数据未能成功渲染成排版。\n错误信息: {error_msg}"
        prs.save(output_file)