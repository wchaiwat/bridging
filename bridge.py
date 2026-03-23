import os
from fastapi import FastAPI, Request
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, FileMessage

app = FastAPI()

# --- These lines now pull from the Render Environment Variables ---
access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.environ.get('LINE_CHANNEL_SECRET')

# IMPORTANT: Replace this with your actual LIFF URL from the LINE Console
LIFF_URL = "https://liff.line.me/2009574246-YjKui6w5" 

CONF = Configuration(access_token=access_token)
HANDLER = WebhookHandler(channel_secret)
# ---------------------------------------------------------------

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()
    HANDLER.handle(body.decode('utf-8'), signature)
    return 'OK'

@HANDLER.add(MessageEvent, message=FileMessage)
def handle_file(event):
    # This grabs the unique ID of the file the user just sent
    file_id = event.message.id
    
    with ApiClient(CONF) as api_client:
        messaging_api = MessagingApi(api_client)
        
        # This sends the link back to the user
        response_text = f"ได้รับไฟล์แล้วครับ! 📊 กดดูวิเคราะห์ได้ที่นี่: {LIFF_URL}?file_id={file_id}"
        
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response_text)]
            )
        )
