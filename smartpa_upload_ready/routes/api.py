"""
api.py
------
定义 Flask 路由，用于处理前端请求：
- /api/chat  -> 接收用户输入，生成 AI 回复
- /api/save  -> 保存 AI 回复为本地 Markdown 文件
- /results/<filename> -> 下载保存的文档
"""

from flask import Blueprint, request, jsonify, send_from_directory
from datetime import datetime
import os

from core.prompt_handler import build_prompt
from core.chat_handler import session_histories, update_chat_history
from utils.openai_helper import generate_prd
from core.save_utils import save_result

api = Blueprint("api", __name__)

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


@api.route("/api/chat", methods=["POST"])
def chat_api():
    try:
        data = request.get_json()
        session_id = data.get("session_id", "default")
        user_input = data.get("message", "")
        task_type = data.get("task_type", "free_chat")

        print(f"🔵 收到请求: session={session_id}, task_type={task_type}")
        print(f"🔵 用户输入: {user_input}")

        if not user_input.strip():
            return jsonify({"error": "内容不能为空"}), 400

        last_task = session_histories.get(f"{session_id}_last_task")
        if last_task and last_task != task_type:
            session_histories[session_id] = []

        history = session_histories.get(session_id, [])
        session_histories[f"{session_id}_last_task"] = task_type

        # 👇 模板任务列表
        template_tasks = [
            "prd", "chat_roleplay", "meeting_summary", "glossary",
            "user_persona", "user_analysis", "journey_map",
            "kickoff_plan", "competitor_analysis", "swot", "storyboard"
        ]

        if task_type in template_tasks:
            from core.prd_generator import generate_prd_from_input
            response_text = generate_prd_from_input(user_input, task_type)
        else:
            from core.prompt_handler import build_prompt
            from utils.openai_helper import generate_prd
            prompt = build_prompt(user_input, task_type, history)
            print("🧪 prompts 内容：\n", prompt)
            response_text = generate_prd(prompt)

        print("🟢 AI 返回：", response_text)
        response_text = response_text.replace("[当前时间]", datetime.now().strftime("%H:%M:%S"))

        update_chat_history(history, user_input, response_text)
        session_histories[session_id] = history

        return jsonify({"reply": response_text})

    except Exception as e:
        import traceback
        print("❌ 出错啦！")
        traceback.print_exc()
        return jsonify({"error": f"❌ 服务器错误：{str(e)}"}), 500



@api.route("/api/save", methods=["POST"])
def save_markdown():
    try:
        data = request.get_json()
        content = data.get("content", "")
        task_type = data.get("task_type", "free_chat")
        session_id = data.get("session_id", "default")

        if not content.strip():
            return jsonify({"error": "内容不能为空"}), 400

        filename = save_result(content, "markdown", task_type, session_id)
        return jsonify({"file_url": f"/results/{filename}"})

    except Exception as e:
        return jsonify({"error": f"❌ 保存失败：{str(e)}"}), 500


@api.route("/results/<path:filename>", methods=["GET"])
def download_result(filename):
    return send_from_directory(RESULTS_DIR, filename, as_attachment=True)
