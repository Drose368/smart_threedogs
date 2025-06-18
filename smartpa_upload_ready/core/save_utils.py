"""
save_utils.py
-------------
用于将 AI 生成内容保存为本地文件，默认格式为 Markdown (.md)。

保存路径: 项目根目录下的 /results 文件夹
"""

import os
import datetime
from typing import Optional

# 统一保存路径
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def save_result(
    content: str,
    format_type: str = "markdown",
    task_type: Optional[str] = None,
    session_id: Optional[str] = None
) -> str:
    """
    将生成结果保存为指定格式的文件（目前支持 Markdown）。

    参数:
        - content: 要保存的文本内容
        - format_type: 保存格式，目前仅支持 "markdown"
        - task_type: 任务类型（例如：prd、swot）
        - session_id: 会话 ID，用于文件命名

    返回:
        - filename: 保存后的文件名（不包含路径）
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    ext = "md" if format_type == "markdown" else "txt"
    filename = f"{task_type or 'task'}_{session_id or 'session'}_{timestamp}.{ext}"
    filepath = os.path.join(RESULTS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filename
