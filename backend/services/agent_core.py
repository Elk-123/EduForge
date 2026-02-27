# backend/services/agent_core.py
import os
import json
import re
from typing import TypedDict, List, Dict, Any, Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from schemas.dsl import PPTDocument, ChatState, ChatResponse, Message

load_dotenv()

# 只定义一次 AgentState（全局）
class AgentState(TypedDict):
    history: List[Dict[str, str]]           # 兼容 Message dict
    file_content: str
    outline: str
    dsl_output: Dict[str, Any]
    intent_complete: bool                   # 用于判断是否进入生成

# LLM 配置（全局）
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3",
    openai_api_key=os.getenv("SILICONFLOW_API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    max_tokens=4096,
    temperature=0.7
)

# CHAT_PROMPT（全局）
CHAT_PROMPT = """
你是一名教学AI智能体，根据赛题要求，通过多轮对话理解教师意图。
对话历史：{history}
用户最新消息：{user_message}
上传文件内容摘要：{file_content}[:2000]...

任务：
- 主动询问澄清模糊需求（如教学目标、知识要点、时长、产出风格、BOPPPS模型等）。
- 如果意图完整（所有关键要素齐备），总结意图，设置is_complete=True，并触发生成DSL。
- 输出严格纯JSON：{{"message": "回复文本", "is_complete": false}} (is_complete=true时，可选包含dsl dict，但这里先不生成，留给generator)

严格遵守原有DSL规则：page_type只限'title'或'content'，总页<8。
"""

# ==================== 工作流定义（模块级，全局可见） ====================
workflow = StateGraph(AgentState)

# chat_node
def chat_node(state: AgentState) -> AgentState:
    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in state.get('history', [])])
    user_message = state['history'][-1]['content'] if state['history'] else "基于上传教案直接生成课件"

    # 自动判断是否需要澄清
    has_file = bool(state.get('file_content', '').strip())
    is_simple_request = len(user_message) < 50 or "直接生成" in user_message or "生成课件" in user_message

    if has_file and is_simple_request:
        # 智能判断：有文件 + 简单请求 → 直接完整
        message = "检测到上传教案且意图清晰，直接基于文件内容生成课件..."
        is_complete = True
        print("DEBUG: 智能判断 - 有文件+简单请求，直接生成！")
    else:
        prompt = f"""
你是一名教学AI智能体，必须严格按赛题要求进行多轮对话澄清教师意图。

当前对话历史：
{history_str}

用户最新消息：{user_message}

上传文件内容摘要（如果有）：{state.get('file_content', '')[:2000]}...

【判断规则】
- 如果有上传教案文件（内容非空）且用户消息简单（无明确要求澄清） → 直接认为意图完整，基于文件生成。
- 否则，必须收集到以下至少3项：
  1. 教学目标
  2. 核心知识点
  3. 课时长度
  4. 教学风格/模型（如BOPPPS）
- 缺项时，主动问1-2个最关键的。
- 输出严格纯JSON，无多余文字！

示例（直接生成）：
{{
  "message": "意图清晰，直接基于教案生成课件...",
  "is_complete": true
}}

示例（需澄清）：
{{
  "message": "请告诉我教学目标和课时长度？",
  "is_complete": false
}}
"""

        response = llm.invoke(prompt)
        raw_content = response.content.strip()

        match = re.search(r'\{[\s\S]*\}', raw_content, re.DOTALL)
        if match:
            try:
                resp_dict = json.loads(match.group(0))
                message = resp_dict.get("message", "正在处理...")
                is_complete = resp_dict.get("is_complete", False)
            except:
                message = "JSON解析失败"
                is_complete = False
        else:
            message = "未找到有效回复"
            is_complete = False

    new_history = state.get("history", []) + [{"role": "assistant", "content": message}]
    state["history"] = new_history
    state["intent_complete"] = is_complete
    return state

# planner_node
def planner_node(state: AgentState):
    intent_summary = "\n".join([m['content'] for m in state['history'] if m['role'] == 'user'])
    prompt = f"""
    你是一名资深教研员。请根据对话意图和文件内容设计一份符合教学逻辑的课件大纲。
    意图总结：{intent_summary}
    内容：{state['file_content'][:2000]}...
    要求：
    1. 输出 Markdown 格式的大纲。
    2. 【极其重要】精简内容，大纲必须控制在 8 页以内！
    """
    response = llm.invoke(prompt)
    print("🎯 [Planner] 大纲规划完成！")
    return {"outline": response.content}

# generator_node
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

# 条件函数
def conditional_entry(state: AgentState):
    if state.get('intent_complete', False):
        return "planner"
    return END

# 添加节点和边（全局）
workflow.add_node("chat", chat_node)
workflow.add_node("planner", planner_node)
workflow.add_node("generator", generator_node)
workflow.set_entry_point("chat")
workflow.add_conditional_edges("chat", conditional_entry, {"planner": "planner", END: END})
workflow.add_edge("planner", "generator")
workflow.add_edge("generator", END)

# 编译（全局 app_agent）
app_agent = workflow.compile()
print("DEBUG: app_agent 已全局编译成功")

class AgentCore:
    def generate_ppt_dsl(self, context_text: str) -> PPTDocument:
        initial_state: AgentState = {
            "history": [{"role": "user", "content": "基于上传教案直接生成"}],  # 让chat_node看到简单请求
            "file_content": context_text,
            "outline": "",
            "dsl_output": {},
            "intent_complete": False
        }

        print("DEBUG: 即将调用全局 app_agent.invoke...")
        final_state = app_agent.invoke(initial_state)  # 使用全局 app_agent
        dsl_dict = final_state.get("dsl_output", {})

        print("DEBUG: final dsl_dict =", dsl_dict)
        print("DEBUG: theme 是否存在？", "theme" in dsl_dict)
        print("DEBUG: pages 是否存在且非空？", bool(dsl_dict.get("pages")))

        try:
            return PPTDocument(**dsl_dict)
        except Exception as e:
            print(f"❌ 转换失败: {e}")
            fallback = {
                "theme": "modern",
                "pages": [{"page_type": "title", "content": {"title": "生成错误，请检查 LLM 输出"}, "notes": str(e)}]
            }
            return PPTDocument(**fallback)

    def process_chat(self, user_message: str, state: AgentState) -> Dict[str, Any]:
        state['history'].append({"role": "user", "content": user_message})
        outputs = app_agent.invoke(state)  # 使用全局 app_agent
        last_message = outputs['history'][-1]['content'] if outputs.get('history') else "错误"
        is_complete = outputs.get('intent_complete', False)
        dsl = outputs.get('dsl_output') if is_complete else None
        return {
            "message": last_message,
            "is_complete": is_complete,
            "dsl": dsl
        }