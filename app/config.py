import os

ELEVENLABS_ENDPOINT = os.getenv(
    "ELEVENLABS_ENDPOINT", "https://api.elevenlabs.io/v1/text-to-speech"
)

GPT_ENDPOINT = os.getenv(
    "GPT_ENDPOINT", "https://tgapi-7d0b0583d985.herokuapp.com/api/v1/llmodels/gpt"
)
