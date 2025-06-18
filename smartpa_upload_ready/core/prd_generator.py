"""
prd_generator.py
----------------
用于根据任务类型加载预设提示词模板，并调用 LLM 生成结果。
"""

import os
from typing import Optional
from utils.openai_helper import generate_prd

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")


def load_prompt_template(task_type: str = "prd_prompt") -> str:
    """
    加载 prompts 目录下的对应模板，例如 prompts/prd_prompt.txt

    参数:
        - task_type: 对应模板名称（不带 .txt）

    返回:
        - 模板文本字符串
    """
    prompt_path = os.path.join(TEMPLATE_DIR, f"{task_type}.txt")

    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ 没找到提示词模板文件: {prompt_path}")


def build_prompt(user_input: str, task_type: str = "prd_prompt") -> str:
    """
    使用模板和用户输入构建完整 prompts

    参数:
        - user_input: 用户输入内容
        - task_type: 对应任务的模板名

    返回:
        - 完整提示词文本
    """
    template = load_prompt_template(task_type)
    user_input_cn = f"（请用简体中文回答）\n{user_input}"
    return template.replace("{user_input}", user_input_cn)


def generate_prd_from_input(user_input: str, task_type: str = "prd_prompt") -> str:
    """
    主函数：根据任务类型构建 prompts 并生成结果

    参数:
        - user_input: 用户输入内容
        - task_type: 任务名，用于加载模板

    返回:
        - AI 生成的内容
    """
    final_prompt = build_prompt(user_input, task_type)
    return generate_prd(final_prompt)
    print("🔧 使用模板任务类型：", task_type)
    print("🔧 最终 prompts：", final_prompt)

