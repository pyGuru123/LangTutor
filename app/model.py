from typing import Optional
from pydantic import BaseModel, Field

class ttsRequest(BaseModel):
    text: str
    model: Optional[str]