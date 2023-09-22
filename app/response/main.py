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
    one_time_keyboard
)


async def main(request: dict):
    audio = None
    text = None

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
        await one_time_keyboard(chat_id)
        await send_bot_action(chat_id)

        if text.strip() == "/start":
            msg = "Hello. From now on ill be your english teacher."
            audio = await generate_audio(msg)
            await send_bot_audio(chat_id, reply_id, audio, caption=msg, title="LangTutor Response")
        else:
            response = await ask_gpt(text)
            if response:
                try:
                    audio = await generate_audio(response)
                    await send_bot_audio(chat_id, reply_id, audio, caption=response, title="LangTutor Response")
                except Exception as e:
                    logger.error(f"{e=}")
                    await send_bot_message(chat_id, reply_id, response)
                    # audio = await generate_audio("An error occured, try again")
                    # await send_bot_audio(chat_id, reply_id, audio)
        