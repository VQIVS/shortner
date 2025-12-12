from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class CreateLinkRequest(BaseModel):
    original_url: HttpUrl
    ttl_seconds: Optional[int] = None 


class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
    clicks: int

    class Config:
        from_attributes = True
