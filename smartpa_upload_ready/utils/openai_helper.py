"""
openai_helper.py
----------------
负责调用 OpenRouter API 与大语言模型通信，返回 AI 生成内容。
"""

import os
from dotenv import load_dotenv
from openai import OpenAI, APIError

# 加载 .env 中的 API 密钥
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("❌ 没有找到 OPENROUTER_API_KEY，请检查 .env 文件")

# 初始化 OpenAI 客户端（使用 OpenRouter 网关）
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


def generate_prd(prompt: str, model: str = "meta-llama/llama-3-8b-instruct") -> str:
    """
    调用 LLM 生成产品相关内容，返回文本结果。

    参数:
        - prompts: 构造好的提示词字符串
        - model: 使用的大模型名称（默认 LLaMA3）

    返回:
        - 生成的文本内容
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    except APIError as e:
        return f"⚠️ OpenRouter API 错误：{str(e)}"

    except Exception as e:
        return f"⚠️ 系统异常，请稍后再试：{str(e)}"
