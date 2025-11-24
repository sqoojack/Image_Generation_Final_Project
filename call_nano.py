
# python3 call_nano.py
import os
import time
from google import genai
from google.genai import types
from PIL import Image  # 引入 PIL
from tqdm import tqdm

# 1. 設定 API Key (要創API_key.txt裡面放你的API key)
def get_api_key(filepath="API_key.txt"):
    try:
        with open(filepath, "r") as f:
            return f.read().strip() # .strip() 可以去除多餘的換行或空白
    except FileNotFoundError:
        print("找不到 API_key.txt")
        return None

os.environ["GOOGLE_API_KEY"] = get_api_key()

client = genai.Client()

# MODEL_ID = "gemini-3-pro-image-preview" 
MODEL_ID = "gemini-2.5-flash-image"
# MODEL_ID = "gemini-2.5-pro"

def generate_dataset_png_only():
    source_dir = "before_images"
    output_dir = "after_images"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prompt 設定
    prompt_mapping = {
        "lego": "Transform this image into a Lego style.",
        "van_gogh": "Redraw this image in the style of Van Gogh's Starry Night.",
    }

    # 取得所有 PNG 檔案
    image_files = sorted([f for f in os.listdir(source_dir) if f.lower().endswith('.png')])

    if not image_files:
        print(f"錯誤: {source_dir} 資料夾中沒有 PNG 圖片。")
        return

    total_tasks = len(image_files) * len(prompt_mapping)

    # 建立進度條
    with tqdm(total=total_tasks, unit="img", desc="Generating") as pbar:
        
        for filename in image_files:
            file_path = os.path.join(source_dir, filename)
            
            # 1. 使用 PIL 讀取圖片
            try:
                source_image = Image.open(file_path)
            except Exception as e:
                tqdm.write(f"Error reading {filename}: {e}")
                # 如果讀圖失敗，要把這張圖對應的風格進度都跳過，以免進度條卡住
                pbar.update(len(prompt_mapping))
                continue

            for style, prompt_text in prompt_mapping.items():
                # 更新進度條描述，讓你知道現在跑到哪張圖、哪個風格
                pbar.set_description(f"Processing {filename} [{style}]")
                
                save_name = f"{os.path.splitext(filename)[0]}_{style}.png"
                save_path = os.path.join(output_dir, save_name)

                try:
                    # 2. 呼叫 API
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=[prompt_text, source_image],
                    )

                    # 3. 解析並儲存結果
                    saved = False
                    if response.parts:
                        for part in response.parts:
                            if part.text is not None:
                                # 若回傳文字，通常代表拒絕生成，用 tqdm.write 顯示
                                tqdm.write(f"  [{filename}-{style}] API Text: {part.text}")
                            
                            elif part.inline_data is not None:
                                generated_image = part.as_image()
                                generated_image.save(save_path)
                                # 這裡不 print 成功訊息，保持乾淨
                                saved = True
                                break 
                    else:
                         tqdm.write(f"  [{filename}-{style}] Empty response (Safety Filter?)")

                    if not saved:
                        tqdm.write(f"  [{filename}-{style}] Failed to save image.")

                    # 避免 Rate Limit
                    # time.sleep(3)

                except Exception as e:
                    tqdm.write(f"  [{filename}-{style}] API Error: {e}")
                    time.sleep(5)
                
                # 完成一個風格，更新進度條
                pbar.update(1)

if __name__ == "__main__":
    generate_dataset_png_only()