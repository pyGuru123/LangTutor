import os
import json
import platform
import requests
import telegram
import assemblyai as aai
from loguru import logger
from telegram import Bot, ReplyKeyboardMarkup
from elevenlabs import generate, play, set_api_key

from app.config import GPT_ENDPOINT

if platform.system() == "Windows":
    from dotenv import load_dotenv

    load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ELEVENLABS_TOKEN = os.environ.get("ELEVENLABS_TOKEN")
ASSEMBLYAI_TOKEN = os.environ.get("ASSEMBLYAI_TOKEN")
set_api_key(ELEVENLABS_TOKEN)
aai.settings.api_key = ASSEMBLYAI_TOKEN

bot = Bot(token=BOT_TOKEN)

async def send_bot_message(chat_id, reply_id, msg):
    response = await bot.send_message(chat_id=chat_id, reply_to_message_id=reply_id, text=msg)
    return response

async def edit_bot_message(chat_id, reply_id, msg):
    response = await bot.edit_message_text(chat_id=chat_id, message_id=reply_id, text=msg)
    return response

async def send_bot_audio(chat_id, reply_id, audio, caption="", title=""):
    response = await bot.send_audio(chat_id=chat_id, reply_to_message_id=reply_id, audio=audio,
                    caption=caption[:512], title=title, performer="LangTutor")
    return response

async def send_bot_action(chat_id):
    await bot.send_chat_action(chat_id=chat_id, action=telegram.constants.ChatAction.UPLOAD_VOICE)

async def get_audio(voice):
    audio = await bot.get_file(voice["file_id"])
    return audio

async def one_time_keyboard(chat_id):
    keyboard = [
        ['English Correction', 'Conversation'],
        ['Word of the Day', 'Translate']
    ]

    markup =  ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await bot.send_message(
            chat_id=chat_id,
            text="I don't understand that command. Please use the Main Menu button.",
            reply_markup=markup
        )

async def ask_gpt(prompt: str):
    payload = json.dumps({
      "context": "I want you to act as an English teacher and help me learn English. \
                I will ask you questions and you will provide explanations, examples, and exercises to\
                improve my English skills",
      "prompt": "Your name is LangTutor and you will Reply me as my english teacher. Try to be as short as possible.\
                 Here's my prompt" + prompt
    })

    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", GPT_ENDPOINT, headers=headers, data=payload)
    return response.json()["content"]

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

async def speech_to_text(file_url):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_url)
    return transcript.text

async def translate_sentence(text: str):
    url = f"https://api.pawan.krd/gtranslate?from=detect&to=sa&text={text}"
    response = requests.get(url)
    return response.json()