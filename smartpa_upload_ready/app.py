import os
from flask import Flask
from flask_cors import CORS
from routes.api import api  # ← 注册蓝图

app = Flask(__name__)
CORS(app)

app.register_blueprint(api)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render 会自动注入 PORT 环境变量
    app.run(host="0.0.0.0", port=port)
