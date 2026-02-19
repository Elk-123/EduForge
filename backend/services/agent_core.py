from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# 定义状态
class AgentState(TypedDict):
    user_input: str
    file_content: str
    outline: str
    dsl_output: dict

# 初始化 DeepSeek (使用 OpenAI SDK 兼容模式)
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key="你的KEY",
    openai_api_base="<https://api.deepseek.com/v1>"
)

# 节点 1: 教学设计规划 (Planner)
def planner_node(state: AgentState):
    prompt = f"""
    你是一名资深教研员。请根据以下内容设计一份符合加涅九步教学法的课件大纲。
    内容：{state['file_content'][:2000]}...
    要求：输出 Markdown 格式的大纲。
    """
    response = llm.invoke(prompt)
    return {"outline": response.content}

# 节点 2: DSL 生成器 (Generator)
def generator_node(state: AgentState):
    prompt = f"""
    根据以下大纲，生成用于 PPT 渲染的 JSON DSL。
    大纲：{state['outline']}

    严格遵守以下 JSON 格式（不要输出 Markdown 代码块，只输出 JSON）：
    {{ "pages": [ {{ "type": "title", "content": {{ ... }} }} ] }}
    """
    # 实际开发中需要使用 Structured Output 或 Pydantic parser 保证 JSON 合法性
    response = llm.invoke(prompt)
    # 这里需要加 try-catch 解析 JSON
    return {"dsl_output": response.content} # 需转换为 dict

# 构建图
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("generator", generator_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "generator")
workflow.add_edge("generator", END)

app_agent = workflow.compile()