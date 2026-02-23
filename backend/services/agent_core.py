# backend/services/agent_core.py
import os
import json
import re
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

load_dotenv()

class AgentState(TypedDict):
    user_input: str
    file_content: str
    outline: str
    dsl_output: dict

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3",
    openai_api_key=os.getenv("SILICONFLOW_API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    max_tokens=4096,  # 🚀 [修改 1] 放大肺活量，从 2048 加到 4096，防止话没说完被截断
    temperature=0.7
)

def planner_node(state: AgentState):
    prompt = f"""
    你是一名资深教研员。请根据以下内容设计一份符合教学逻辑的课件大纲。
    内容：{state['file_content'][:2000]}...
    要求：
    1. 输出 Markdown 格式的大纲。
    2. 【极其重要】精简内容，大纲必须控制在 8 页以内！
    """
    response = llm.invoke(prompt)
    print("🎯 [Planner] 大纲规划完成！")
    return {"outline": response.content}

def generator_node(state: AgentState):
    prompt = f"""
    根据以下大纲，生成用于 PPT 渲染的 JSON DSL。
    大纲：{state['outline']}

    【最高指令】你必须严格遵守以下 3 条规则：
    1. page_type 只能是 "title" 或 "content"！绝对不能写 section, media, diagram 等词汇！
    2. 幻灯片总数不得超过 8 页！
    3. 必须输出完整闭合的纯 JSON，不要包含 ```json 这样的 Markdown 标记。

    标准格式示例：
    {{
      "theme": "modern",
      "pages": [
        {{ "page_type": "title", "content": {{ "title": "主标题", "subtitle": "副标题" }}, "notes": "备注" }},
        {{ "page_type": "content", "content": {{ "title": "内容标题", "items": ["要点1", "要点2"] }}, "notes": "备注" }}
      ]
    }}
    """
    response = llm.invoke(prompt)
    raw_content = response.content
    
    match = re.search(r'\{[\s\S]*\}', raw_content)
    
    if match:
        json_str = match.group(0).strip()
        try:
            dsl_dict = json.loads(json_str)
            print("🎯 [Generator] JSON DSL 提取且解析成功！")
        except json.JSONDecodeError as e:
            # 🚀 [修改 2] 防截断自愈补丁：如果刚好断在对象结尾 }，强行补上数组和外层闭合
            try:
                print(f"⚠️ [Generator] 触发防截断修复机制...")
                repaired_json = json_str + "\n  ]\n}"
                dsl_dict = json.loads(repaired_json)
                print("🎯 [Generator] 截断 JSON 修复成功！")
            except Exception as e2:
                print(f"❌ [Generator] JSON 彻底解析失败: {e2}")
                dsl_dict = {"theme": "modern", "pages": [{"page_type": "title", "content": {"title": "AI解析失败", "subtitle": "JSON格式不规范"}, "notes": ""}]}
    else:
        print(f"❌ [Generator] 完全找不到 JSON 结构！")
        dsl_dict = {"theme": "modern", "pages": [{"page_type": "title", "content": {"title": "未找到JSON", "subtitle": "请重试"}, "notes": ""}]}
        
    return {"dsl_output": dsl_dict}

workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("generator", generator_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "generator")
workflow.add_edge("generator", END)

app_agent = workflow.compile()

from schemas.dsl import PPTDocument

class AgentCore:
    def generate_ppt_dsl(self, context_text: str) -> PPTDocument:
        initial_state = {
            "user_input": "生成一份PPT",
            "file_content": context_text,
            "outline": "",
            "dsl_output": {}
        }
        
        final_state = app_agent.invoke(initial_state)
        dsl_dict = final_state["dsl_output"]
        
        # 将安全的 dict 转为 Pydantic 对象供渲染器使用
        try:
            return PPTDocument(**dsl_dict)
        except Exception as e:
            print(f"❌ [AgentCore] 数据结构转换失败 (可能是产生了非法的 page_type): {e}")
            fallback_dict = {"theme": "modern", "pages": [{"page_type": "title", "content": {"title": "数据模型错误", "subtitle": str(e)}, "notes": ""}]}
            return PPTDocument(**fallback_dict)