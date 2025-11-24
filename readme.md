

### 0. 建立環境
```pip install -r requirements.txt```

### 1. 準備圖片:
將原圖放入 raw_before_images/

### 2. 預處理:
```python preprocessing.py```
統一轉為 PNG (512x512) 結果會存入 before_images/
以確保模型輸入的一致性

### 3. 設定key:
建立 API_key.txt，內容貼上 Google API Key

### 4. 執行生成:
```python call_nano.py```
結果會存在 after_images/


### 5. 產出比較圖:
```python compare.py```
產生 compare.png