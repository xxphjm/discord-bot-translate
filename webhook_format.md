# Make.com Webhook 格式說明

## 請求格式 (Request Format)

Discord機器人會向Make.com webhook發送以下格式的JSON請求：

```json
{
  "text": "要翻譯的文字內容",
  "target_lang": "目標語言代碼"  // 可選，如果指定則翻譯成該語言，否則由Make.com自動偵測
}
```

### 請求標頭 (Request Headers)
```
Authorization: Bearer X7kP9mN3vL2qR5tY8wJ4hB6gF0dC1aE2uI9oT3rM5nV7xZ
Content-Type: application/json
```

### 範例請求：
```json
{
  "text": "Hello, how are you?",
  "target_lang": "ko"
}
```

```json
{
  "text": "Hello, how are you?"
}
```

## 回應格式 (Response Format)

Make.com webhook應該回傳以下格式的JSON回應：

```json
{
  "korean": "韓文翻譯結果",
  "vietnamese": "越文翻譯結果", 
  "chinese": "中文翻譯結果"
}
```

### 範例回應：
```json
{
  "korean": "안녕하세요, 잘 지내세요?",
  "vietnamese": "Chào bạn, bạn khỏe không?",
  "chinese": "你好，你好嗎？"
}
```

## Make.com Prompt 範例

在Make.com的AI模組中，可以使用以下prompt來進行翻譯：

```
請將以下文字翻譯成韓文、越文和繁體中文。如果提供了目標語言代碼，請優先翻譯成該語言，並同時提供其他兩種語言的翻譯。請以JSON格式回傳結果，格式如下：

{
  "korean": "韓文翻譯",
  "vietnamese": "越文翻譯", 
  "chinese": "繁體中文翻譯"
}

要翻譯的文字：{{text}}
目標語言代碼 (可選)：{{target_lang}}

注意事項：
1. 請保持翻譯的準確性和自然性
2. 如果原文是韓文、越文或中文，請翻譯成其他兩種語言
3. 請確保回傳的JSON格式正確
4. 中文請使用繁體中文
5. 請直接回傳JSON，不要包含其他文字說明
```

## 設定步驟

### 1. 建立Make.com Scenario
1. 登入Make.com
2. 建立新的scenario
3. 選擇「Webhooks」作為trigger

### 2. 設定Webhook Trigger
1. 選擇「Custom webhook」
2. 複製webhook URL：`https://hook.eu2.make.com/woprpcgkuw7degky8vovtmz1tdznwtf0`
3. 設定認證：新增一個或多個API金鑰，使用HTTP標頭 `x-make-apikey` 傳送。

### 3. 新增AI翻譯模組
1. 新增「OpenAI」或其他AI服務模組
2. 設定API金鑰
3. 選擇適當的模型（建議GPT-3.5-turbo或GPT-4）
4. 在prompt欄位貼上上述的prompt範例
5. 將webhook接收到的`text`欄位映射到prompt中的`{{text}}`
6. 將webhook接收到的`target_lang`欄位映射到prompt中的`{{target_lang}}` (如果存在)

### 4. 設定回應模組
1. 新增「Webhooks」回應模組
2. 設定回應格式為JSON
3. 確保回傳包含korean、vietnamese、chinese三個欄位

### 5. 測試和啟用
1. 儲存scenario
2. 啟用scenario
3. 使用測試程式驗證功能

## 錯誤處理

如果webhook回傳錯誤或格式不正確，Discord機器人會顯示錯誤訊息。請確保：

### 常見錯誤和解決方法

1. **401 Unauthorized**
   - 檢查API金鑰是否正確
   - 確認Make.com scenario已啟用
   - 檢查webhook URL是否正確

2. **500 Internal Server Error**
   - 檢查AI模組的API金鑰是否有效
   - 確認prompt格式正確
   - 檢查AI服務是否有足夠的配額

3. **JSON格式錯誤**
   - 確保AI回應只包含JSON格式
   - 檢查回應是否包含所有必要欄位
   - 確認沒有額外的文字說明

### 測試方法

使用提供的測試程式檢查webhook：
```bash
python test_webhook.py
```

預期的成功回應：
- Status Code: 200
- 包含korean、vietnamese、chinese三個欄位的JSON回應

## 安全注意事項

1. 妥善保管API金鑰和webhook URL
2. 定期檢查Make.com的使用配額
3. 監控webhook的請求頻率，避免超出限制
4. 建議在生產環境中使用HTTPS
5. 考慮實作請求頻率限制以防止濫用

