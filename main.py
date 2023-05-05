from fastapi import FastAPI, Request, Header
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from starlette.exceptions import HTTPException
from mangum import Mangum
import gpt
import os
import uvicorn


app = FastAPI(title="ChatGPT君", description="LineからChatGPTを利用します。")
lambda_handler = Mangum(app)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])


@app.get("/")
def root():
    return {"title": app.title, "description": app.description}


@app.post("/")
def callback(request: Request):
    return "OK"


@app.post(
    "/callback",
    summary="LINE Message APIからのコールバックです。",
    description="ユーザーからメッセージが送信された際、LINE Message APIからこちらのメソッドが呼び出されます。",
)
async def callback(request: Request, x_line_signature=Header(None)):
    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = gpt.inquire_gpt(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, TextMessage(text=msg))


# ローカル開発用
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
