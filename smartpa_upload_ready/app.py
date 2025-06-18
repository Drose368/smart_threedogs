from flask import Flask
from flask_cors import CORS
from routes.api import api

app = Flask(__name__)
CORS(app)

# ✅ 添加一个首页路由，测试是否运行成功
@app.route("/")
def index():
    return "SmartPA 后端已部署成功 🎉"

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
