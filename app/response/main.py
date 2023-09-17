import json
from loguru import logger

from app.response.utils import (
    send_bot_message,
    edit_bot_message,
    send_bot_audio,
    generate_audio,
    send_bot_action,
    ask_gpt,
    get_audio,
    speech_to_text
)


async def main(request: dict):
    audio = None
    text = None

    content = request["content"]
    chat_id = content["message"]["chat"]["id"]
    reply_id = content["message"]["message_id"]

    if "text" in content["message"]:
        text = content["message"]["text"]
    elif "voice" in content["message"]:
        audio = await get_audio(content["message"]["voice"])
        text = await speech_to_text(audio.file_path)

    if text:
        logger.info(text)
        await send_bot_action(chat_id)

        if text.strip() == "/start":
            audio = await generate_audio("Hello. From now on ill be your english teacher.")
            await send_bot_audio(chat_id, reply_id, audio)
        else:
            if audio:
                message = await send_bot_message(chat_id, reply_id, "Query : " + text)

            response = await ask_gpt(text)
            if response:
                if audio:
                    await edit_bot_message(chat_id, message.message_id, "Response : " + response)

                try:
                    reply_audio = await generate_audio(response)
                    await send_bot_audio(chat_id, reply_id, reply_audio)
                except Exception as e:
                    logger.error(f"{e=}")
        