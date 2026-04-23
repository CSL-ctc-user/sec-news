import os
import vertexai
from vertexai.generative_models import GenerativeModel
from flask import Flask, request, jsonify

app = Flask(__name__)

# 元の関数を維持
def summarize_with_gemini(text):
    locations = ["asia-northeast1", "us-central1"]
    model_names = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-1.5-flash-002"]
    
    for loc in locations:
        vertexai.init(project="my-project-csl-486600", location=loc)
        for model_name in model_names:
            try:
                model = GenerativeModel(model_name)
                # モデルの呼び出しテスト
                model.generate_content("hello")
                response = model.generate_content(f"要約してください: {text}")
                return response.text
            except Exception:
                continue
    return "Error: No model could be accessed."

# Cloud Run がPOSTリクエストを受け取るためのルート定義
@app.route("/", methods=["POST"])
def summarize_endpoint():
    # ユーザーからのJSONを受け取る
    data = request.get_json()
    # {"name": "Developer"} が送られてくる想定
    text_to_process = data.get("name", "Developer")
    
    # 処理を実行
    summary = summarize_with_gemini(text_to_process)
    
    # 結果を返す
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
