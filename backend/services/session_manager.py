# 新建 backend/services/session_manager.py (内存会话管理，简单不引入额外依赖)
import uuid
from typing import Dict, Optional
from schemas.dsl import ChatState

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ChatState] = {}

    def get_or_create(self, session_id: Optional[str] = None) -> tuple[str, ChatState]:
        if not session_id:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = ChatState()
        return session_id, self.sessions.get(session_id, ChatState())

    def update(self, session_id: str, state: ChatState):
        self.sessions[session_id] = state

session_mgr = SessionManager()  # 单例实例