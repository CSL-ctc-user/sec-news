def summarize_with_gemini(text):
    # 東京(asia-northeast1)と米国(us-central1)の両方を試す
    locations = ["asia-northeast1", "us-central1"]
    # 試すモデル名（バージョン番号を外したものも含める）
    model_names = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-1.5-flash-002"]
    
    for loc in locations:
        vertexai.init(project="my-project-csl-486600", location=loc)
        for model_name in model_names:
            try:
                print(f"Trying: {model_name} in {loc}")
                model = GenerativeModel(model_name)
                # モデルの呼び出しテスト（空のプロンプトで試す）
                model.generate_content("hello")
                print(f"!!! SUCCESS: {model_name} works in {loc} !!!")
                # 成功したらそれを使う
                response = model.generate_content(f"要約してください: {text}")
                return response.text
            except Exception as e:
                print(f"Failed: {model_name} in {loc} - {e}")
                continue
    
    return "Error: No model could be accessed."
