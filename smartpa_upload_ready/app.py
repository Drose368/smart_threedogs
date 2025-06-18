from flask import Flask
from flask_cors import CORS
from routes.api import api  # 注册蓝图

app = Flask(__name__)
CORS(app)

# 注册蓝图
app.register_blueprint(api)

# ✅ 加一个默认首页
@app.route('/')
def home():
    return "部署成功啦！这是聪明的三狗 SmartPA 🎉"

if __name__ == "__main__":
    app.run(debug=True)
