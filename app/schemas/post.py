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
    nickname : str
    profile_image_url : str

class LikeToggle(BaseModel):
    """
    좋아요 등록/해제 반환 모델
    """
    message : str
    is_liked : bool
    likes_count : int

class PostResponse(BaseModel):
    """
    게시물 리스폰스 모델
    """
    post_id: int
    user_id: str
    image_urls: List[HttpUrl]
    content: Optional[str]
    uploaded_at: datetime
    liked_by: List[Like]

class FamousResponse(BaseModel):
    """
    인기 멍멍이 피드 반환 모델
    """
    post_id: int
    user_id: str
    user_name: str
    image_urls: List[HttpUrl]
    liked_by: List[Like]

class PostCreate(BaseModel):
    """
    게시물 생성 모델
    """
    image_urls: List[str] # base64 encoding string을 받아야 하므로
    content: Optional[str]

class PostUpdate(BaseModel):
    """
    게시물 수정 모델
    """
    content: str