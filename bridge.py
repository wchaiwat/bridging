from fastapi import FastAPI, Request
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, MessagingApiBlob, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, FileMessage

app = FastAPI()

# --- ใส่ข้อมูลของคุณตรงนี้ ---
CONF = Configuration(access_token='ก๊อปปี้ Access Token มาวางที่นี่')
HANDLER = WebhookHandler('ก๊อปปี้ Channel Secret มาวางที่นี่')
LIFF_URL = "https://liff.line.me/YOUR_LIFF_ID" # ใส่ LIFF ID ของคุณ
# -----------------------

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()
    HANDLER.handle(body.decode('utf-8'), signature)
    return 'OK'

@HANDLER.add(MessageEvent, message=FileMessage)
def handle_file(event):
    # ดึง File ID เพื่อส่งต่อไปยัง Streamlit
    file_id = event.message.id
    
    with ApiClient(CONF) as api_client:
        messaging_api = MessagingApi(api_client)
        # ส่งข้อความตอบกลับพร้อมลิงก์ LIFF
        response_text = f"ได้รับไฟล์แล้วครับ! 📊 กดดูวิเคราะห์ได้ที่นี่: {LIFF_URL}?file_id={file_id}"
        
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response_text)]
            )
        )