"""
prompt_handler.py
-----------------
构建用于大模型调用的提示词（prompts）。

核心功能：
- 根据任务类型（如：PRD、竞品分析）生成带上下文的 prompts
"""

from typing import List, Dict

def build_prompt(user_input: str, task_type: str, history: List[Dict[str, str]] = None) -> str:
    """
    构建大模型调用所需的 prompts，包含任务类型、对话历史、用户输入。

    参数:
        - user_input: 当前用户输入
        - task_type: 本次任务类型（如“产品需求文档”）
        - history: 上下文历史（最近 6 轮）

    返回:
        - prompts: 构造好的完整提示词字符串
    """

    history_text = ""
    if history:
        for turn in history[-6:]:
            role = "用户" if turn["role"] == "user" else "助手"
            history_text += f"{role}：{turn['content']}\n"

    prompt = (
        f"你是一位全能型的项目与产品专家，请用简体中文回答用户的所有问题，风格友好、专业，必要时也可以幽默轻松。\n"
        f"当前任务类型是：{task_type}\n"
        f"以下是之前的对话历史：\n{history_text}\n"
        f"现在用户说：{user_input}\n"
        f"请根据上下文理解用户意图，继续生成或修改内容："
    )

    return prompt
