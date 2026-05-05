# Discord 翻譯機器人

這是一個Discord聊天機器人，能夠自動將訊息翻譯成韓文、越文和中文。機器人使用Make.com的webhook進行翻譯處理。

## 功能特色

- **自動翻譯訊息**：直接發送純文字訊息，機器人會自動偵測語言並翻譯成韓文、越文、繁體中文，並回覆給發送者。
- **手動翻譯**：使用 `!translate <語言代碼> <文字>` 指令，指定翻譯目標語言。
- **查看支援語言**：使用 `!languages` 指令，查看機器人支援的語言代碼列表。
- **測試Make.com連接**：使用 `!test_make` 指令，測試機器人與Make.com webhook的連接狀態。
- **非文字內容檢測**：機器人會自動跳過圖片、連結、表情符號等非純文字內容的翻譯。
- 使用 `!` 前綴觸發指令
- 整合Make.com webhook進行AI翻譯
- 支援多語言輸入

## 安裝步驟

1. 安裝Python依賴套件：
```bash
pip install -r requirements.txt
```

2. 設定環境變數：
   - `DISCORD_TOKEN`：你的Discord機器人Token
   - `API_KEY`：你的Make.com API金鑰 

3. 確保Make.com webhook已正確設定並可接收請求 (請參考 `webhook_format.md`)

## 使用方法

1. 啟動機器人：
```bash
python bot.py
```

2. 在Discord頻道中使用：
   - **自動翻譯**：直接發送純文字訊息，例如：`Hello, how are you?`
   - **手動翻譯**：`!translate ko 你好` (將「你好」翻譯成韓文)
   - **查看支援語言**：`!languages`
   - **測試連接**：`!test_make`
   - **一般指令翻譯**：`!要翻譯的文字` (例如：`!Hello, how are you?`)

3. 機器人會回覆翻譯結果或相關資訊。

## 設定說明

### Discord機器人設定

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 建立新的應用程式和機器人
3. 複製機器人Token
4. 邀請機器人到你的Discord伺服器，需要以下權限：
   - Send Messages
   - Read Message History
   - Use Slash Commands

### Make.com Webhook設定

請參考 `webhook_format.md` 文件了解詳細的webhook設定方法。

## 檔案結構

- `bot.py` - 主要的Discord機器人程式
- `requirements.txt` - Python依賴套件清單
- `webhook_format.md` - Make.com webhook格式說明
- `test_webhook.py` - webhook測試程式
- `README.md` - 使用說明文件

## 故障排除

### 常見問題

1. **機器人無法連接Discord**
   - 檢查Discord Token是否正確
   - 確認機器人已被邀請到伺服器

2. **翻譯功能無法運作**
   - 檢查Make.com webhook URL是否正確
   - 確認webhook已正確設定並啟用
   - 檢查API金鑰是否有效

3. **401 Unauthorized錯誤**
   - 確認Make.com webhook的認證設定，應使用 `x-make-apikey` 標頭傳送金鑰。
   - 檢查API金鑰是否正確。

4. **500 Internal Server Error (Scenario failed to complete)**
   - 檢查Make.com Scenario內部邏輯，確保AI模組和回應模組設定正確。
   - 確認AI服務的API金鑰有效且有足夠配額。
   - 確保AI回傳的JSON格式符合預期。

### 測試webhook

使用提供的測試程式檢查webhook連接：
```bash
python test_webhook.py
```

預期的成功回應：
- Status Code: 200
- 包含korean、vietnamese、chinese三個欄位的JSON回應

## 部署選項

### 本地運行
直接在本地電腦運行：
```bash
python bot.py
```

### 雲端部署
可以部署到以下平台（建議使用）：
- Heroku
- Railway
- Replit
- DigitalOcean
- AWS EC2

部署時請確保：
1. 設定正確的環境變數 (`DISCORD_TOKEN`, `API_KEY`)
2. 安裝所有依賴套件 (`pip install -r requirements.txt`)
3. 確保伺服器可以訪問外部API
4. 機器人程式持續運行 (例如使用 `nohup python bot.py &` 或 PM2 等進程管理工具)

## 注意事項

- 機器人需要持續運行才能回應訊息
- Make.com webhook需要有效的訂閱才能正常運作
- 請妥善保管Discord Token和API金鑰
- 建議在生產環境中使用環境變數管理敏感資訊

### 📝 **查看支援語言**
```
!languages
```
這個指令會顯示機器人支援的所有語言代碼和對應的語言名稱。

### 🔄 **自動翻譯**
直接發送純文字訊息，機器人會自動翻譯成韓文、越文、繁體中文，並回覆給發送者。

### 🎯 **手動翻譯**
```
!translate <語言代碼> <文字>
```
例如：
- `!translate ko 你好` (將「你好」翻譯成韓文)
- `!translate vi Hello` (將「Hello」翻譯成越文)
- `!translate zh-TW Hello` (將「Hello」翻譯成繁體中文)

### 🧪 **測試Make.com連接**
```
!test_make
```
這個指令會測試機器人與Make.com webhook的連接狀態。

### ⚡ **一般指令翻譯**
```
!<要翻譯的文字>
```
例如：
- `!Hello, how are you?`
- `!你好嗎？`

機器人會將文字翻譯成韓文、越文、繁體中文並回覆。

### ❓ **幫助指令**
```
!help
```
顯示所有指令的說明，包含多語言翻譯。

