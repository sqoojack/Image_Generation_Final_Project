
# python Code/compare.py
# 用來做出比較圖
import os
from PIL import Image, ImageDraw, ImageFont

def create_column_comparison():
    # --- 設定路徑 ---
    source_dir = "before_images"
    generated_dir = "after_images"
    output_filename = "compare.png"
    
    # --- 設定樣式順序 ---
    # 垂直堆疊順序: [原圖] -> [Lego] -> [Van Gogh]
    styles = ["lego", "van_gogh", "water_color", "robot", "solid gold"] 
    
    # --- 設定顯示參數 ---
    target_width = 400   # 每一張圖的寬度 (也是每一行的寬度)
    padding = 20         # 行與行之間的間距
    vertical_gap = 5     # 同一行內，上下圖片的間距
    font_size = 30
    
    # 取得並排序原始圖片
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.png')]
    image_files.sort()

    if not image_files:
        print("找不到原始圖片")
        return

    print(f"正在製作直行比較圖，共 {len(image_files)} 行 (Columns)...")

    # 載入字型
    try:
        font = ImageFont.truetype("Arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 用來存放每一「行 (Column)」合併好的長條圖
    columns = []

    for filename in image_files:
        base_name = os.path.splitext(filename)[0]
        
        # 1. 準備這一行 (Column) 的三張圖片路徑與標籤
        # 結構: [(路徑, 標籤), (路徑, 標籤), (路徑, 標籤)]
        col_items = [
            (os.path.join(source_dir, filename), f"{filename}"),
        ]
        
        for style in styles:
            style_filename = f"{base_name}_{style}.png"
            col_items.append(
                (os.path.join(generated_dir, style_filename), style.capitalize())
            )

        # 2. 處理這一行的圖片 (垂直堆疊)
        imgs_in_col = []
        
        for file_path, label in col_items:
            try:
                if os.path.exists(file_path):
                    img = Image.open(file_path).convert("RGB")
                    
                    # 等比例縮放至 target_width
                    ratio = target_width / float(img.width)
                    new_h = int(img.height * ratio)
                    img = img.resize((target_width, new_h), Image.Resampling.LANCZOS)
                    
                    # 加上文字標籤
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([(0,0), (target_width, 40)], fill="black")
                    draw.text((10, 5), label, fill="white", font=font)
                    
                    imgs_in_col.append(img)
                else:
                    # Missing
                    blank = Image.new('RGB', (target_width, target_width), (50, 50, 50))
                    draw = ImageDraw.Draw(blank)
                    draw.text((10, 50), "Missing", fill="white", font=font)
                    imgs_in_col.append(blank)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

        # 3. 建立這一行 (Column) 的畫布
        # 總高度 = 所有圖片高度總和 + 間距
        total_col_height = sum(img.height for img in imgs_in_col) + (vertical_gap * (len(imgs_in_col) - 1))
        col_img = Image.new('RGB', (target_width, total_col_height), (255, 255, 255))
        
        # 將圖片垂直貼上
        current_y = 0
        for img in imgs_in_col:
            col_img.paste(img, (0, current_y))
            current_y += img.height + vertical_gap
            
        columns.append(col_img)

    if not columns:
        return

    # 4. 合併所有行 (橫向合併)
    # 總寬度 = (行寬 * 數量) + (行距 * (數量-1))
    total_width = (target_width * len(columns)) + (padding * (len(columns) - 1))
    # 總高度 = 最高的那一行
    max_height = max(c.height for c in columns)
    
    final_image = Image.new('RGB', (total_width, max_height), (255, 255, 255))
    
    current_x = 0
    for col in columns:
        final_image.paste(col, (current_x, 0))
        current_x += col.width + padding

    final_image.save(output_filename)
    print(f"完成！已儲存為: {output_filename}")

if __name__ == "__main__":
    create_column_comparison()