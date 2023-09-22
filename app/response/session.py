from loguru import logger
from pydantic import BaseModel
from datetime import datetime, timedelta

session_data = {}

class SessionData(BaseModel):
    user_id: str
    documents: list
    page: int
    message_id: int
    expiration: datetime

async def create_session(user_id: str, message_id, documents: list = [], page=1):
    session_token = f"user:{user_id}"
    expiration = datetime.now() + timedelta(minutes=3)
    session_data[session_token] = SessionData(user_id=user_id, 
                                    documents=documents, 
                                    page=page, 
                                    message_id=message_id,
                                    expiration=expiration)
    return session_token

async def update_session(user_id: str, page):
    session_token = f"user:{user_id}"
    session_data[session_token].page = page 
    return session_token

async def get_user_from_session(session_token: str):
    session = session_data.get(session_token)
    if session is None:
        return None
    return session.documents, session.page, session.message_id

async def cleanup_sessions():
    now = datetime.now()
    expired_sessions = [session_token for session_token, session in session_data.items()
                             if session.expiration < now]
    for session_token in expired_sessions:
        del session_data[session_token]

    logger.info(f"session active : {len(session_data.keys())}")