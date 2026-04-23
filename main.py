import os
import requests
from flask import Flask, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)

# Secret Managerから環境変数として読み込む
# ※Cloud Runの設定でこれらの環境変数を指定してください
GRAPH_API_TOKEN = os.environ.get("GRAPH_API_TOKEN") 
TOCARO_WEBHOOK_URL = os.environ.get("TOCARO_WEBHOOK_URL")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

def get_sharepoint_content():
    # ※ここにMicrosoft Graph APIを呼び出すロジックを実装
    # 今回は簡略化のためダミーテキストを返します
    return "【要約対象のセキュリティニュース本文...】"

def summarize_with_gemini(text):
    vertexai.init(project=PROJECT_ID, location="asia-northeast1")
    model = GenerativeModel("gemini-1.5-pro")
    
    prompt = f"以下のセキュリティニュースを、要点のみ箇条書きで3行に要約してください：\n{text}"
    response = model.generate_content(prompt)
    return response.text

def send_to_tocaro(message):
    payload = {"text": message}
    requests.post(TOCARO_WEBHOOK_URL, json=payload)

@app.route("/", methods=["POST"])
def run_pipeline():
    try:
        # 1. コンテンツ取得
        content = get_sharepoint_content()
        # 2. 要約
        summary = summarize_with_gemini(content)
        # 3. 通知
        send_to_tocaro(summary)
        return jsonify({"status": "success", "summary": summary}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
