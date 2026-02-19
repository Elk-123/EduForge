from pptx import Presentation
from pptx.util import Inches, Pt
import json
import os

class PPTRenderer:
    def __init__(self, template_path=None):
        # 如果没有模板，使用默认空白模板
        self.prs = Presentation(template_path) if template_path and os.path.exists(template_path) else Presentation()

    def create_slide(self, page_data):
        """根据 DSL 类型分发渲染逻辑"""
        # PPTX 默认母版索引: 0=标题页, 1=标题+内容页
        layout_map = {"title": 0, "content_list": 1} 
        
        # 获取布局，如果没有对应的类型，默认使用类型 1
        layout_index = layout_map.get(page_data.get('type'), 1)
        slide_layout = self.prs.slide_layouts[layout_index]
        slide = self.prs.slides.add_slide(slide_layout)

        content = page_data.get('content', {})

        # --- 通用逻辑: 设置标题 ---
        # 并不是所有版式都有标题占位符，先判断一下
        if slide.shapes.title and 'title' in content:
            slide.shapes.title.text = content['title']

        # --- 针对 "title" (封面页) 的特殊逻辑 ---
        if page_data['type'] == 'title':
            # 尝试找副标题占位符 (通常是占位符索引 1)
            if len(slide.placeholders) > 1 and 'subtitle' in content:
                slide.placeholders[1].text = content['subtitle']

        # --- 针对 "content_list" (正文列表) 的特殊逻辑 ---
        if page_data['type'] == 'content_list':
            # 尝试找正文文本框 (通常是占位符索引 1)
            if len(slide.placeholders) > 1 and 'items' in content:
                body_shape = slide.placeholders[1]
                tf = body_shape.text_frame
                tf.clear() # 清除默认文本

                for item in content['items']:
                    p = tf.add_paragraph()
                    p.text = item
                    p.level = 0 # 缩进级别

        # --- 添加演讲者备注 (Notes) ---
        if 'notes' in page_data:
            if slide.has_notes_slide:
                notes_slide = slide.notes_slide
                text_frame = notes_slide.notes_text_frame
                text_frame.text = page_data['notes']

    def render(self, dsl_json: dict, output_file: str):
        # 容错处理：确保 pages 存在
        if 'pages' not in dsl_json:
            print("Error: Invalid DSL format, missing 'pages'")
            return

        for page in dsl_json['pages']:
            self.create_slide(page)
        
        self.prs.save(output_file)
        print(f"✅ PPT 生成成功: {output_file}")
        return output_file

# --- 测试入口 ---
if __name__ == "__main__":
    # 这里定义真实的测试数据 (Dict)，而不是 { ... }
    mock_data = {
      "theme": "dark_modern",
      "pages": [
        {
          "type": "title",
          "content": {
            "title": "牛顿第二定律",
            "subtitle": "高中物理必修一 / 讲师：AI老师"
          },
          "notes": "开场白：同学们好，今天我们来学习力学中最核心的定律。"
        },
        {
          "type": "content_list",
          "content": {
            "title": "本节课目标",
            "items": [
                "1. 理解 F=ma 的物理含义", 
                "2. 掌握控制变量法的实验设计", 
                "3. 能够应用公式解决基础力学问题"
            ]
          },
          "notes": "这里要强调一下控制变量法的重要性。"
        }
      ]
    }

    renderer = PPTRenderer()
    renderer.render(mock_data, "test_output.pptx")