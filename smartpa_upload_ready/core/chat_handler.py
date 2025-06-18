"""
chat_handler.py
---------------
用于存储和维护多轮对话的上下文历史，用于构建更自然的 AI 回复。

结构设计：
- session_histories：用 session_id（用户）来区分对话线程
"""

from typing import Dict, List

# 会话上下文结构：{session_id: [{"role": "user", "content": ...}, {"role": "assistant", "content": ...}]}
session_histories: Dict[str, List[Dict[str, str]]] = {}


def init_chat_history() -> List[Dict[str, str]]:
    """
    初始化一个新的聊天历史
    """
    return []


def update_chat_history(history: List[Dict[str, str]], user_input: str, response: str) -> None:
    """
    向历史中添加新的用户输入和 AI 回复

    参数:
        - history: 当前会话历史列表
        - user_input: 用户输入
        - response: AI 生成的回复
    """
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
