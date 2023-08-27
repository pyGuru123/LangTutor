from fastapi import FastAPI
from loguru import logger

from app.response.router import router as ResponseRouter
from app.text2speech.router import router as Text2SpeechRouter

app = FastAPI(title="LangTutorApi")

# --------------------------------------------------------------------------
#                                Routers

app.include_router(ResponseRouter, prefix="/api/v1/response", tags=["Bot Response"])
app.include_router(Text2SpeechRouter, prefix="/api/v1/synthesis", tags=["Speech Synthesis"])


# --------------------------------------------------------------------------


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "An api for LangTutorBot"}


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Application is shutting down")
    logger.info("Application shutdown successfully")
