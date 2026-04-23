import os
import requests
from flask import Flask, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)

# Cloud Run の環境変数から値を取得
GRAPH_API_TOKEN = os.environ.get("GRAPH_API_TOKEN") 
TOCARO_WEBHOOK_URL = os.environ.get("TOCARO_WEBHOOK_URL")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

def get_sharepoint_content():
    # 本番用のロジックをここに記載
    return "【要約対象のセキュリティニュース本文...】"

def summarize_with_gemini(text):
    # バージョン番号なしの「gemini-1.5-pro」を指定することで404を回避
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash")
    
    prompt = f"以下のセキュリティニュースを、要点のみ箇条書きで3行に要約してください：\n{text}"
    response = model.generate_content(prompt)
    return response.text

def send_to_tocaro(message):
    payload = {"text": message}
    requests.post(TOCARO_WEBHOOK_URL, json=payload)

@app.route("/", methods=["POST"])
def run_pipeline():
    try:
        content = get_sharepoint_content()
        summary = summarize_with_gemini(content)
        send_to_tocaro(summary)
        return jsonify({"status": "success", "summary": summary}), 200
    except Exception as e:
        # エラー発生時も500を返してログを残す
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
