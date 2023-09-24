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
    speech_to_text,
    one_time_keyboard,
    translate_sentence
)


async def main(request: dict):
    audio = None
    text = None
    response = None

    content = request["content"]
    chat_id = content["message"]["chat"]["id"]
    reply_id = content["message"]["message_id"]

    logger.info(content)

    await send_bot_action(chat_id)

    if "text" in content["message"]:
        text = content["message"]["text"]
    elif "voice" in content["message"]:
        voice = await get_audio(content["message"]["voice"])
        text = await speech_to_text(voice.file_path)

    if text:
        logger.info(text)
        await send_bot_action(chat_id)

        if text.strip() == "/start":
            response = "Hello. From now on ill be your english teacher."
        if text.startswith("/translate"):
            text = text.remove("/translate")
            response = translate_sentence(text)
        else:
            response = await ask_gpt(text)

        try:
            await send_bot_action(chat_id)
            audio = await generate_audio(response)
            await send_bot_audio(chat_id, reply_id, audio, caption=response, title="LangTutor Response")
        except Exception as e:
            logger.error(f"{e=}")
            await send_bot_message(chat_id, reply_id, response)
        