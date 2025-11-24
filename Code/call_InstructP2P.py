
# python Code/call_InstructP2P.py
import os
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline
from PIL import Image

def generate_dataset():
    # 1. 設定路徑
    source_dir = "before_images"       # 你剛剛裁切好的 512x512 原圖資料夾
    output_dir = "after_images"     # 存放生成結果的資料夾
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. 載入 InstructPix2Pix 模型 (這是專門做修圖的 AI)
    # 第一次跑會下載模型，約需幾分鐘
    model_id = "timbrooks/instructpix2pix"
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
        model_id, 
        torch_dtype=torch.float16
    ).to("cuda") # 確保你有用 GPU

    # 為了省記憶體
    pipe.enable_attention_slicing()

    # 3. 定義你的 Prompts (這裡放你剛剛想好的清單)
    # 格式: (類別名稱, Prompt)
    object_prompts = [
        ("lego", "Transform this image into a Lego style."),
        ("van_gogh", "Redraw this image in the style of Van Gogh's Starry Night."),
        # ("sketch", "Turn this into a pencil sketch"),
        # ... 把你那 10 個 object prompt 放進來
    ]
    
    landscape_prompts = [
        ("winter", "Make it a snowy winter scene"),
        ("sunset", "Make it a sunset scene with golden hour lighting"),
        # ... 把你那 10 個 landscape prompt 放進來
    ]

    # 4. 開始批次處理
    images = os.listdir(source_dir)
    
    for filename in images:
        if not filename.endswith((".png", ".jpg")):
            continue
            
        file_path = os.path.join(source_dir, filename)
        original_image = Image.open(file_path).convert("RGB")
        
        # 判斷這張圖是用哪一組 prompt (這需要你分類好，或簡化處理)
        # 假設你目前混在一起跑，我們先用 object_prompts 做示範
        # 實際操作建議分兩個資料夾：source_objects 和 source_landscapes
        
        # 這裡以 Object 為例
        target_prompts = object_prompts 
        
        print(f"Processing: {filename}...")
        
        for style_name, prompt_text in target_prompts:
            # 設定檔名: cat_01_lego.png
            base_name = os.path.splitext(filename)[0]
            save_name = f"{base_name}_{style_name}.png"
            save_path = os.path.join(output_dir, save_name)
            
            # 如果已經生過就跳過 (斷點續傳)
            if os.path.exists(save_path):
                continue

            # 生成圖片
            # image_guidance_scale: 控制要多像原圖 (越小越不像，太大改不動)
            # guidance_scale: 控制要多聽 Prompt 的話
            edited_image = pipe(
                prompt_text, 
                image=original_image, 
                num_inference_steps=20, 
                image_guidance_scale=1.5,  # 關鍵參數
                guidance_scale=7.5
            ).images[0]
            
            edited_image.save(save_path)
            print(f"  -> Generated: {save_name}")

if __name__ == "__main__":
    generate_dataset()