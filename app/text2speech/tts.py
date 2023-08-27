import json
import requests
from loguru import logger

from app.config import ELEVENLABS_ENDPOINT

ELEVEN_LAB_MODELS = {
	"daniel": "onwK4e9ZLuTAKqWW03F9",
	"callum": "N2lVS1w4EtoT3dr4eOWO",
	"charlie": "IKne3meq5aSn9XLyUdCD",
	"charlotte": "XB0fDUnXU5powFXDhCwa",
	"clyde": "2EiwWnXFnvU5JabPnv8n",
	"emily": "LcfcDJNUP1GQjkzn1xUU",
	"freya": "jsCqWAovK2LkecY7zXl4",
	"serena": "pMsXgVXv3BLzUgSXRplE"
}

def get_elevenlab_model(model):
    if not model:
        return ELEVEN_LAB_MODELS.get("emily", "")

    return ELEVEN_LAB_MODELS.get(model, "LcfcDJNUP1GQjkzn1xUU")

async def elevenlab_all_models():
	return list(ELEVEN_LAB_MODELS.keys())

async def text_to_speech(text, model):
	payload = json.dumps({
	  "text": text,
	  "model_id": "eleven_multilingual_v2"
	})

	headers = {
	  'Content-Type': 'application/json'
	}

	model_id = get_elevenlab_model(model)

	url = f"{ELEVENLABS_ENDPOINT}/{model_id}/stream"
	logger.info(url)

	response = requests.request("POST", ELEVENLABS_ENDPOINT, headers=headers, data=payload)
	logger.info(response.status_code)
	logger.info(response.text)
	return response.content