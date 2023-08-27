from fastapi import APIRouter, BackgroundTasks
from typing import Union
from fastapi.responses import Response
from loguru import logger

from app.response.main import main

router = APIRouter()


@router.post("/reply")
async def reply(request: dict, background_tasks: BackgroundTasks):
    """Replying to bot commands"""
    try:
        background_tasks.add_task(main, request)
        return {"message": "success"}
    except Exception as e:
        return {"message": "error", "error": str(e)}