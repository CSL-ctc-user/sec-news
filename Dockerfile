# 軽量なPython環境を指定
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係ファイルをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをすべてコピー
COPY . .

# Cloud Run が使用するポート（通常 8080）で Gunicorn を起動
# workers=1, threads=8 は小規模なツールに最適な設定です
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
