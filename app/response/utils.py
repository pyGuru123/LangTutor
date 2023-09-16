import os
import json
import platform
import requests
from telegram import Bot
from elevenlabs import generate, play, set_api_key

from app.config import GPT_ENDPOINT

if platform.system() == "Windows":
    from dotenv import load_dotenv

    load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ELEVENLABS_TOKEN = os.environ.get("ELEVENLABS_TOKEN")
set_api_key(ELEVENLABS_TOKEN)

bot = Bot(token=BOT_TOKEN)

async def send_bot_message(chat_id, reply_id, msg):
    await bot.send_message(chat_id=chat_id, reply_to_message_id=reply_id, text=msg)

async def send_bot_audio(chat_id, reply_id, audio):
    await bot.send_audio(chat_id=chat_id, reply_to_message_id=reply_id, audio=audio)

async def ask_gpt(prompt: str):
    payload = json.dumps({
      "prompt": "reply to this prompt as my english teacher in under 500 characters only \n" + prompt
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", GPT_ENDPOINT, headers=headers, data=payload)
    return response.json()["choices"][0]["message"]["content"]

async def generate_audio(text: str):
    if text:
        audio = generate(
          text=text,
          voice="Bella",
          model="eleven_monolingual_v1"
        )
    else:
        audio = generate(
          text="Sorry i was unable to get you",
          voice="Bella",
          model="eleven_monolingual_v1"
        )

    return audio