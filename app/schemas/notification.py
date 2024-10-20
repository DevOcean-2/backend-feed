"""
알림 API 스키마
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from app.schemas.post import Like


class NotiType(str, Enum):
    """
    알림 타입
    """
    NOTI_TYPE_MISSION = "mission"
    NOTI_TYPE_FEED = "feed"


class NotiTypeFeed(BaseModel):
    """
    피드 알림 모델
    """
    feed_id: int
    likes: Optional[List[Like]]


class NotiTypeMission(BaseModel):
    """
    미션 알림 모델
    """
    mission: str
    is_success: bool


class NotiResponse(BaseModel):
    """
    알림 모델
    """
    noti_type: NotiType
    is_read: bool = False
    noti_detail: Union[NotiTypeFeed, NotiTypeMission]
    created_at: datetime
