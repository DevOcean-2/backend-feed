"""
게시물 API 스키마
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class Like(BaseModel):
    """
    좋아요 모델
    """
    user_id: str
    nickname: str
    profile_image_url: Optional[HttpUrl]


class PostResponse(BaseModel):
    """
    게시물 리스폰스 모델
    """
    post_id: int
    image_urls: List[HttpUrl]
    content: Optional[str]
    uploaded_at: datetime
    liked_by: List[Like]


class PostCreate(BaseModel):
    """
    게시물 생성 모델
    """
    image_urls: List[HttpUrl]
    content: Optional[str]


class PostUpdate(BaseModel):
    """
    게시물 수정 모델
    """
    content: str
