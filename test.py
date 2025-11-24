from google import genai
import os

# 1. 設定你的 API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBIaDmCGIAH-Hkn5chPmEgDnll_gigWpRQ"
client = genai.Client()

print("正在查詢可用的模型 (New SDK)...\n")

# 3. 列出模型
# 新版 SDK 使用 client.models.list()
try:
    pager = client.models.list()
    
    for model in pager:
        # 簡單過濾：只印出 Gemini 和 Imagen 系列，避免印出一大堆舊模型
        if "gemini" in model.name or "imagen" in model.name:
            print(f"Model Name:   {model.name}")
            print(f"Display Name: {model.display_name}")
            print("-" * 30)

except Exception as e:
    print(f"查詢失敗: {e}")