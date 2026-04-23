import os
import vertexai
from vertexai.generative_models import GenerativeModel
from flask import Flask, request, jsonify

app = Flask(__name__)

# 元の関数を維持
def summarize_with_gemini(text):
    locations = ["asia-northeast1", "us-central1"]
    model_names = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-1.5-flash-002"]
    
    errors = [] # エラーを記録するリスト
    
    for loc in locations:
        vertexai.init(project="my-project-csl-486600", location=loc)
        for model_name in model_names:
            try:
                model = GenerativeModel(model_name)
                model.generate_content("hello")
                response = model.generate_content(f"要約してください: {text}")
                return response.text
            except Exception as e:
                # エラー内容を記録
                error_msg = f"{loc}/{model_name}: {str(e)}"
                errors.append(error_msg)
                print(error_msg) # ログにも出す
                continue
    
    # 全部失敗したらエラーメッセージを返す
    return "Error: " + " | ".join(errors)

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
