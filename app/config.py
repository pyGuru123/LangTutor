import os

ELEVENLABS_ENDPOINT = os.getenv(
    "ELEVENLABS_ENDPOINT", "https://api.elevenlabs.io/v1/text-to-speech"
)

GPT_ENDPOINT = os.getenv(
    "GPT_ENDPOINT", "https://movieshub-e2d380615f80.herokuapp.com/api/v1/llmodels/gpt"
)
