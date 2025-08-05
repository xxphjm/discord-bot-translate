# Discord翻譯機器人 - Railway部署指南

## 概述

這個版本的Discord翻譯機器人是一個基於Python的應用程式，可以部署到Railway平台。它將持續運行以監聽Discord訊息並進行翻譯。

## 部署步驟

### 1. 準備GitHub儲存庫

1. 將以下檔案上傳到GitHub儲存庫的根目錄：
   - `bot.py` (機器人主程式)
   - `requirements.txt` (Python依賴)
   - `Procfile` (Railway啟動指令)
   - `railway.json` (Railway設定檔)
   - `webhook_format.md` (Make.com Webhook格式說明)
   - `README.md` (專案說明)
   - `test_webhook.py` (Webhook測試腳本)

### 2. 在Railway中部署

1. 前往 [Railway Dashboard](https://railway.app/dashboard)
2. 點擊「New Project」
3. 選擇「Deploy from GitHub Repo」
4. 選擇你的GitHub儲存庫
5. Railway會自動偵測到這是一個Python專案並使用 `Procfile` 和 `railway.json` 進行部署

### 3. 設定環境變數

在Railway專案設定中，新增以下環境變數：

- `DISCORD_TOKEN`：你的Discord機器人Token
- `MAKE_API_KEY`：你的Make.com API金鑰 (`X7kP9mN3vL2qR5tY8wJ4hB6gF0dC1aE2uI9oT3rM5nV7xZ`)

### 4. 設定Discord應用程式

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 選擇你的應用程式
3. 在「Bot」頁面中：
   - 複製Bot Token並設定為Railway環境變數
4. 在「OAuth2 > URL Generator」中：
   - 選擇 `bot` 權限
   - 選擇 `Send Messages` 和 `Read Message History` 權限
   - 使用生成的URL邀請機器人到伺服器

## 使用方法

部署完成後，機器人將自動運行。在Discord頻道中，你可以使用以下方式與機器人互動：

- **自動翻譯**：直接發送純文字訊息，機器人會自動翻譯成韓文、越文、繁體中文。
- **手動翻譯**：`!translate <語言代碼> <文字>` (例如: `!translate ko 你好`)
- **查看支援語言**：`!languages`
- **測試Make.com連接**：`!test_make`

## 故障排除

### 1. 機器人無法啟動

- 檢查Railway日誌，查看是否有錯誤訊息。
- 確保 `requirements.txt` 中的所有依賴都已正確安裝。
- 檢查 `Procfile` 中的啟動指令是否正確 (`web: python bot.py`)。

### 2. 翻譯功能無法運作

- 檢查Railway環境變數 `DISCORD_TOKEN` 和 `MAKE_API_KEY` 是否正確設定。
- 檢查Make.com webhook是否正常運作，並確保其設定與 `webhook_format.md` 一致。
- 檢查Railway日誌，查看是否有與Make.com連接相關的錯誤。

### 3. 檢查Railway日誌

1. 前往Railway Dashboard
2. 選擇你的專案
3. 點擊「Deployments」標籤
4. 查看最新部署的日誌以診斷問題

## 優勢

- **持續運行**：適合需要長時間監聽訊息的Discord機器人。
- **易於部署**：Railway提供簡單的GitHub整合部署。
- **環境變數管理**：方便管理敏感資訊。

## 注意事項

1. 確保Make.com webhook已正確設定並可接收請求。
2. 定期檢查Railway和Make.com的使用配額。
3. 妥善保管Discord Token和API金鑰。
4. 建議在生產環境中使用環境變數管理敏感資訊。

