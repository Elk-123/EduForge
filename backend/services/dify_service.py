# backend/services/dify_service.py
import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

class DifyWorkflowClient:
    def __init__(self):
        self.api_key = os.getenv("DIFY_API_KEY")
        self.base_url = "https://api.dify.ai/v1/workflows/run"

    # 将原来的一次性返回方法改为异步生成器 (yield)
    async def stream_eduforge_workflow(
        self, 
        subject: str, 
        task_type: str = "outline", 
        refined_outline: str = "", 
        user_id: str = "eduforge_user"
    ):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": {
                "subject": subject,
                "task_type": task_type,
                "refined_outline": refined_outline
            },
            "response_mode": "streaming",  # 【关键修改1】改为流式
            "user": user_id
        }
        
        # 增加整体 timeout 限制，但因为是流式，只要保持数据传输就不会轻易触发 504
        timeout = httpx.Timeout(120.0, connect=60.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            # 【关键修改2】使用 stream 发送请求
            async with client.stream("POST", self.base_url, headers=headers, json=payload) as response:
                
                # 如果 Dify 报 401 或 500 等错误，提前拦截
                if response.status_code != 200:
                    error_msg = await response.aread()
                    yield f"Error: 请求 Dify 失败 (状态码 {response.status_code})。详情: {error_msg.decode('utf-8')}"
                    return

                # 【关键修改3】逐行读取并解析 Dify 的 SSE 数据流
                async for line in response.aiter_lines():
                    # Dify 的流式数据以 "data: " 开头
                    if line.startswith("data: "):
                        try:
                            # 截取 "data: " 后面的 JSON 字符串进行解析
                            data_str = line[6:]
                            data_obj = json.loads(data_str)
                            
                            event_type = data_obj.get("event")
                            
                            # 当节点正在输出文本块时 (text_chunk)
                            if event_type == "text_chunk":
                                text = data_obj.get("data", {}).get("text", "")
                                if text:
                                    yield text  # 将文本片段实时推给路由
                                    
                            # 工作流执行出错
                            elif event_type == "error":
                                error_msg = data_obj.get("data", {}).get("error", "未知错误")
                                yield f"\n\n[Dify 工作流错误: {error_msg}]"
                                break
                                
                            # 节点或工作流结束时，可以不做处理，或者打印日志
                            elif event_type == "workflow_finished":
                                break

                        except json.JSONDecodeError:
                            # 忽略无法解析的行
                            continue
                        except Exception as e:
                            print(f"解析流式数据异常: {e}")
                            continue