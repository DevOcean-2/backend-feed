"""
알림 API 스키마
"""
from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.post import Like


class NotiResponse(BaseModel):
    """
    알림 모델
    """
    is_read: bool = False
    created_at: datetime

    post_id: int
    likes: List[Like]
