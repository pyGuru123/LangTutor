from fastapi import APIRouter
from typing import Union
from fastapi.responses import Response
from loguru import logger

from app.model import ttsRequest
from app.text2speech.tts import (
    text_to_speech,
    elevenlab_all_models
) 

router = APIRouter()


@router.post("/tts")
async def tts(request: ttsRequest):
    """Convert Text to speech with ElevenLabs Api"""
    try:
        text = request.text
        model = request.model
        audio_bytes = await text_to_speech(text, model)

        headers = {
            "Content-Disposition": "attachment; filename=generated_audio.wav"
        }

        return Response(
            content=audio_bytes, media_type="audio/wav", headers=headers
        )
    except Exception as e:
        return {"message": "error", "text": text, "content": None, "error": str(e)}

@router.get("/tts/models")
async def tts_models() -> dict:
    """Returns a list of models that can be used with /tts endpoint"""
    return {"message": "success", "models": await elevenlab_all_models()}
