# backend/services/agent_core.py
import os
import json
import re
from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from services.rag_service import rag_service # 引入 RAG 服务

load_dotenv()

# 添加 session_id 用于 RAG 检索
class AgentState(TypedDict):
    session_id: str                         
    history: List[Dict[str, str]]           
    file_content: str
    outline: str
    dsl_output: Dict[str, Any]
    intent_complete: bool                   

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3",
    openai_api_key=os.getenv("SILICONFLOW_API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    max_tokens=4096,
    temperature=0.7
)

workflow = StateGraph(AgentState)

# 1. Chat Node (意图收集)
def chat_node(state: AgentState) -> AgentState:
    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in state.get('history', [])])
    user_message = state['history'][-1]['content'] if state['history'] else "基于上传教案直接生成"

    has_file = bool(state.get('file_content', '').strip())
    is_simple_request = len(user_message) < 50 or "直接生成" in user_message or "生成课件" in user_message

    if has_file and is_simple_request:
        message = "检测到已上传教材且意图清晰，正在为您检索知识库并生成课件大纲..."
        is_complete = True
    else:
        prompt = f"""
你是一名教学AI智能体。必须通过多轮对话澄清教师意图。
对话历史：\n{history_str}
用户最新消息：{user_message}

【判断规则】
- 若用户要求直接生成，或已收集到教学目标、重点等，则认为意图完整。
- 若缺项，请主动提问（1-2个问题）。
- 必须输出严格 JSON：{{"message": "回复文本", "is_complete": false}}
"""
        response = llm.invoke(prompt)
        match = re.search(r'\{[\s\S]*\}', response.content.strip(), re.DOTALL)
        if match:
            try:
                resp = json.loads(match.group(0))
                message = resp.get("message", "正在处理...")
                is_complete = resp.get("is_complete", False)
            except:
                message = "解析失败，请重试。"
                is_complete = False
        else:
            message = "意图已收集，准备生成。"
            is_complete = True

    new_history = state.get("history", []) + [{"role": "assistant", "content": message}]
    return {"history": new_history, "intent_complete": is_complete}

# 2. Planner Node (🌟 核心：去向量库检索并规划大纲)
def planner_node(state: AgentState):
    session_id = state.get("session_id", "default")
    # 提取用户的核心诉求作为 Query
    intent_summary = "\n".join([m['content'] for m in state['history'] if m['role'] == 'user'])
    
    # 🌟 核心：去 RAG 向量库检索相关教材内容
    retrieved_context = rag_service.retrieve_context(session_id, intent_summary)
    context_to_use = retrieved_context if retrieved_context else state.get('file_content', '')[:1000]

    prompt = f"""
    你是一名资深教研员。请根据对话意图和以下检索到的【真实教材内容】设计课件大纲。
    
    用户意图/要求：{intent_summary}
    检索到的参考教材内容：
    {context_to_use}
    
    要求：
    1. 输出 Markdown 格式大纲。
    2. 【极其重要】精简内容，控制在 8 页以内！
    """
    response = llm.invoke(prompt)
    print("🎯 [Planner] 结合 RAG 知识，大纲规划完成！")
    return {"outline": response.content}

# 3. Generator Node (生成渲染 JSON)
# 将这段代码替换掉原来的 generator_node 函数
def generator_node(state: AgentState):
    prompt = f"""
    根据以下大纲，生成用于 PPT 渲染的 JSON DSL。
    大纲：{state['outline']}
    
    【最高指令 - 极其重要】：
    1. page_type 只能是 "title" 或 "content"！绝对不能用其他的！
    2. 幻灯片总数不得超过 8 页！
    3. 必须输出合法、闭合的 JSON 格式！
    4. 直接输出 JSON 字符串，**绝对不要**包含任何 Markdown 标记（如 ```json）！
    
    标准格式示例：
    {{
        "theme": "modern",
        "pages": [
            {{
                "page_type": "title",
                "content": {{ "title": "主标题", "subtitle": "副标题" }},
                "notes": "备注"
            }},
            {{
                "page_type": "content",
                "content": {{ "title": "内容标题", "items": ["要点1", "要点2"] }},
                "notes": "备注"
            }}
        ]
    }}
    """
    response = llm.invoke(prompt)
    raw_content = response.content.strip()
    
    # 🌟 新增：在终端打印 AI 原始输出，方便排错
    print("\n" + "="*40)
    print("🤖 [Generator] AI 原始输出截取(前300字):")
    print(raw_content[:300] + "...")
    print("="*40 + "\n")

    # 🌟 增强版 JSON 提取与清洗机制
    # 1. 尝试匹配 Markdown 代码块中的 JSON
    md_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_content, re.DOTALL)
    if md_match:
        json_str = md_match.group(1).strip()
    else:
        # 2. 如果没有代码块，直接用贪婪模式抓取大括号
        bracket_match = re.search(r'\{[\s\S]*\}', raw_content)
        if bracket_match:
            json_str = bracket_match.group(0).strip()
        else:
            json_str = ""

    if json_str:
        try:
            dsl_dict = json.loads(json_str)
            print("🎯 [Generator] 成功：JSON DSL 解析完美！")
        except json.JSONDecodeError as e:
            print(f"❌ [Generator] 失败：JSON 格式依然有误: {e}")
            print(f"❌ [Generator] 导致报错的残缺 JSON 是:\n{json_str}")
            dsl_dict = {
                "theme": "modern", 
                "pages": [{"page_type": "title", "content": {"title": "JSON格式化失败，请查看控制台日志"}, "notes": ""}]
            }
    else:
        print("❌ [Generator] 失败：AI 返回的内容中完全找不到 JSON 结构！")
        dsl_dict = {
            "theme": "modern", 
            "pages": [{"page_type": "title", "content": {"title": "未生成有效数据，请重试"}, "notes": ""}]
        }

    return {"dsl_output": dsl_dict}

def conditional_entry(state: AgentState):
    return "planner" if state.get('intent_complete', False) else END

# 编译图
workflow.add_node("chat", chat_node)
workflow.add_node("planner", planner_node)
workflow.add_node("generator", generator_node)
workflow.set_entry_point("chat")
workflow.add_conditional_edges("chat", conditional_entry, {"planner": "planner", END: END})
workflow.add_edge("planner", "generator")
workflow.add_edge("generator", END)

app_agent = workflow.compile()

class AgentCore:
    def process_chat(self, user_message: str, session_id: str, state_dict: Dict[str, Any]) -> Dict[str, Any]:
        """处理对话并返回结果"""
        # 构建符合要求的 AgentState
        agent_state: AgentState = {
            "session_id": session_id,
            "history": state_dict.get("history", []),
            "file_content": state_dict.get("file_content", ""),
            "outline": state_dict.get("outline", ""),
            "dsl_output": state_dict.get("current_dsl") or {},
            "intent_complete": False
        }
        agent_state['history'].append({"role": "user", "content": user_message})
        
        # 运行图
        outputs = app_agent.invoke(agent_state)
        
        last_message = outputs['history'][-1]['content'] if outputs.get('history') else "错误"
        is_complete = outputs.get('intent_complete', False)
        dsl = outputs.get('dsl_output') if is_complete else None
        
        return {
            "message": last_message,
            "is_complete": is_complete,
            "dsl": dsl,
            "history": outputs['history'],
            "outline": outputs.get('outline', "")
        }