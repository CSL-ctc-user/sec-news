import vertexai
from vertexai.generative_models import GenerativeModel

# デバッグ用関数
def list_available_models():
    # プロジェクトで利用可能なモデルを確認するための簡単なロジック
    print("Checking available models...")
    # 実際にはモデルのメタデータを確認するAPIを叩きますが、
    # シンプルに「使えるモデルをログに出す」だけでもヒントになります
    # 成功すればここを通ります
    pass

# 実行時に以下を確認できるようにする
# vertexai.init(project=PROJECT_ID, location="us-central1")
# print("Initialization complete.")
