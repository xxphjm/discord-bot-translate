import discord
import os
import requests
import re
import pandas as pd

TOKEN = os.environ.get("DISCORD_TOKEN", "NA")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "NA")
API_KEY = os.environ.get("WEBHOOK_API_KEY", "NA")

SUPPORTED_LANGUAGES = {
    "ko": "韓文",
    "vi": "越文",
    "zh-TW": "繁體中文",
    "en": "英文"
}

def is_text_only(content):
    """檢查訊息是否只包含文字內容"""
    # 移除空白字符
    content = content.strip()
    
    # 如果內容為空，返回False
    if not content:
        return False
    
    # 檢查是否包含URL
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    if re.search(url_pattern, content):
        return False
    
    # 檢查是否只包含表情符號或特殊字符
    # 移除常見的標點符號和空格後，檢查是否還有實際文字內容
    text_only = re.sub(r'[^\w\s\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]', '', content)
    if len(text_only.strip()) < 2:  # 如果實際文字內容少於2個字符，視為非文字
        return False
    
    return True

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # 檢查是否有附件（圖片、文件等）
    if message.attachments:
        return  # 如果有附件，不進行翻譯

    # 檢查是否有嵌入內容（如連結預覽）
    if message.embeds:
        return  # 如果有嵌入內容，不進行翻譯

    if message.content.startswith("!help"):
        async with message.channel.typing():
            print("開始處理 !help 指令，顯示輸入狀態")
            
            # 幫助訊息以 JSON 格式定義
            help_json = pd.read_json("help.json")
            print(help_json)
            # 檢查是否有指定語言參數
            content_parts = message.content.split()
            target_lang = None
            if len(content_parts) > 1 and content_parts[1].startswith("--"):
                lang_param = content_parts[1].lstrip("--").lower()
                if lang_param in ["ko", "korean", "韓文"]:
                    target_lang = "korean"
                elif lang_param in ["vi", "vietnamese", "越南語"]:
                    target_lang = "vietnamese"
                elif lang_param in ["zh", "zh-tw", "chinese", "中文", "繁體中文"]:
                    target_lang = "chinese"
            
            # 根據指定語言回應對應的幫助訊息
            if target_lang and target_lang in help_json:
                help_text = f"{help_json[target_lang]['title']}\n{help_json[target_lang]['content'].strip()}"
                await message.reply(help_text)
            else:
                # 如果未指定語言，顯示所有語言的幫助訊息
                full_help_message = "**多語言說明**\n\n"
                for lang in help_json:
                    full_help_message += f"{help_json[lang]['title']}\n{help_json[lang]['content'].strip()}\n\n"
                await message.reply(full_help_message)
            
            print("結束處理 !help 指令，輸入狀態應結束")
        return

    if message.content.startswith("!languages"):
        async with message.channel.typing():
            lang_list = "\n".join([f"{code}: {name}" for code, name in SUPPORTED_LANGUAGES.items()])
            await message.channel.send(f"支援的語言代碼：\n{lang_list}")
            return

    if message.content.startswith("!test_make"):
        async with message.channel.typing():
            try:
                headers = {
                    "x-make-apikey": API_KEY,
                    "Content-Type": "application/json"
                }
                
                test_data = {"text": "Hello, this is a test message."}
                response = requests.post(WEBHOOK_URL, json=test_data, headers=headers)
                
                if response.status_code == 200:
                    try:
                        json_response = response.json()
                        await message.channel.send("✅ Make.com連接測試成功！\n翻譯服務正常運作。")
                    except ValueError:
                        await message.channel.send("⚠️ Make.com連接成功，但回應格式不正確。")
                else:
                    await message.channel.send(f"❌ Make.com連接測試失敗！\n狀態碼: {response.status_code}")
            except requests.exceptions.RequestException as e:
                await message.channel.send(f"❌ Make.com連接測試失敗！\n錯誤: {e}")
            return

    if message.content.startswith("!translate"):
        async with message.channel.typing():
            # 解析 !translate 指令
            parts = message.content.split(" ", 2)
            if len(parts) < 3:
                await message.channel.send("使用方法: `!translate <語言代碼> <文字>`\n例如: `!translate ko 你好`")
                return
            
            target_lang = parts[1].lower()
            text_to_translate = parts[2]
            
            if target_lang not in SUPPORTED_LANGUAGES:
                await message.channel.send(f"不支援的語言代碼: {target_lang}\n使用 `!languages` 查看支援的語言")
                return
            
            if not is_text_only(text_to_translate):
                await message.channel.send("⚠️ 只能翻譯純文字內容")
                return
            
            try:
                headers = {
                    "x-make-apikey": API_KEY,
                    "Content-Type": "application/json"
                }
                
                # 發送指定語言的翻譯請求
                response = requests.post(WEBHOOK_URL, json={
                    "text": text_to_translate,
                    "target_lang": target_lang
                }, headers=headers)
                response.raise_for_status()
                
                translated_texts = response.json()
                
                # 根據指定語言顯示翻譯結果
                if target_lang == "ko" and "korean" in translated_texts:
                    await message.channel.send(f"🇰🇷 {translated_texts['korean']}")
                elif target_lang == "vi" and "vietnamese" in translated_texts:
                    await message.channel.send(f"🇻🇳 {translated_texts['vietnamese']}")
                elif target_lang == "zh-tw" and "chinese" in translated_texts:
                    await message.channel.send(f"🇹🇼 {translated_texts['chinese']}")
                else:
                    # 如果沒有指定語言的翻譯，顯示所有翻譯
                    korean_text = translated_texts.get("korean", "N/A")
                    vietnamese_text = translated_texts.get("vietnamese", "N/A")
                    chinese_text = translated_texts.get("chinese", "N/A")
                    await message.reply(f"🇰🇷 {korean_text}\n🇻🇳 {vietnamese_text}\n🇹🇼 {chinese_text}")
                    
            except requests.exceptions.RequestException as e:
                await message.channel.send(f"翻譯服務錯誤: {e}")
            except ValueError:
                await message.channel.send("翻譯服務回應格式錯誤")
            return

        # 其他以!開頭的指令，進行一般翻譯
        text_to_translate = message.content[1:].strip()
        if text_to_translate:
            if not is_text_only(text_to_translate):
                await message.channel.send("⚠️ 只能翻譯純文字內容")
                return
                
            try:
                headers = {
                    "x-make-apikey": API_KEY,
                    "Content-Type": "application/json"
                }
                
                response = requests.post(WEBHOOK_URL, json={"text": text_to_translate}, headers=headers)
                response.raise_for_status()
                
                translated_texts = response.json()
                
                korean_text = translated_texts.get("korean", "N/A")
                vietnamese_text = translated_texts.get("vietnamese", "N/A")
                chinese_text = translated_texts.get("chinese", "N/A")

                await message.reply(f"🇰🇷 {korean_text}\n🇻🇳 {vietnamese_text}\n🇹🇼 {chinese_text}")
            except requests.exceptions.RequestException as e:
                await message.channel.send(f"翻譯服務錯誤: {e}")
            except ValueError:
                await message.channel.send("翻譯服務回應格式錯誤")
    else:
        async with message.channel.typing():
            # 自動翻譯功能 - 對於非指令的一般訊息
            if not is_text_only(message.content):
                return  # 如果不是純文字內容，不進行翻譯
            
            try:
                headers = {
                    "x-make-apikey": API_KEY,
                    "Content-Type": "application/json"
                }
                
                response = requests.post(WEBHOOK_URL, json={"text": message.content}, headers=headers)
                response.raise_for_status()
                
                translated_texts = response.json()
                
                korean_text = translated_texts.get("korean", "N/A")
                vietnamese_text = translated_texts.get("vietnamese", "N/A")
                chinese_text = translated_texts.get("chinese", "N/A")

                await message.reply(f"🇰🇷 {korean_text}\n🇻🇳 {vietnamese_text}\n🇹🇼 {chinese_text}")
                
            except requests.exceptions.RequestException as e:
                await message.channel.send(f"翻譯服務錯誤: {e}")
            except ValueError:
                await message.channel.send("翻譯服務回應格式錯誤")

client.run(TOKEN)


