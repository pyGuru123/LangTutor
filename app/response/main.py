import json
from loguru import logger

from app.response.utils import (
    send_bot_message,
    send_bot_audio,
    generate_audio,
    ask_gpt
)


async def main(request: dict):
    content = request["content"]
    chat_id = content["message"]["chat"]["id"];
    text = content["message"]["text"];
    reply_id = content["message"]["message_id"];
    logger.info(f"{text=}")

    response = await ask_gpt(text)
    logger.info(f"{response=}")
    if response:
        audio = await generate_audio(response)
        await send_bot_audio(chat_id, reply_id, audio)
        