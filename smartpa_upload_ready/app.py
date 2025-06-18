from flask import Flask
from flask_cors import CORS
from routes.api import api

app = Flask(__name__)
CORS(app)

# ✅ 添加这个首页路由，解决白屏问题
@app.route("/")
def index():
    return "SmartPA 后端部署成功！🎉"

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
