
# python Code/preprocessing.py
# 將圖片都改成.png檔, 解析度都統一改成512x512, 大小也是512x512, 以確保模型輸入的一致性
import os
from PIL import Image

def preprocess_images(source_folder, target_folder, target_size=512):
    """
    將 source_folder 裡的所有圖片：
    1. 短邊縮放到 target_size
    2. 中心裁切成 target_size x target_size
    3. 存到 target_folder
    """
    
    # 如果目標資料夾不存在，就建立它
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    for filename in os.listdir(source_folder):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in valid_extensions:
            continue

        img_path = os.path.join(source_folder, filename)
        
        try:
            with Image.open(img_path) as img:
                # 轉成 RGB (避免 PNG 透明背景或 RGBA 造成問題)
                img = img.convert("RGB")
                
                # 1. 計算縮放比例 (以短邊為準)
                w, h = img.size
                scale = target_size / min(w, h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                
                # 使用 LANCZOS 濾鏡進行高品質縮放
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # 2. 中心裁切
                left = (new_w - target_size) // 2
                top = (new_h - target_size) // 2
                right = left + target_size
                bottom = top + target_size
                
                img = img.crop((left, top, right, bottom))
                
                # 3. 存檔 (建議統一存成 png 以免壓縮失真)
                # 檔名保持原樣，或者你可以在這裡改名
                save_path = os.path.join(target_folder, os.path.splitext(filename)[0] + ".png")
                img.save(save_path)
                print(f"Processed: {filename} -> {save_path}")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    source_folder = "raw_before_images"    # 把原始大圖放在這個資料夾
    target_folder = "before_images"  # 處理好的圖會放在這個資料夾
    preprocess_images(source_folder=source_folder, target_folder=target_folder)