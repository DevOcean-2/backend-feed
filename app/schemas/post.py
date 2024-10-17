"""
게시물 API 스키마
"""
from pydantic import BaseModel


class PostResponse(BaseModel):
    """
    게시물 리스폰스 모델
    """


class PostCreate(BaseModel):
    """
    게시물 생성 모델
    """


class PostUpdate(BaseModel):
    """
    게시물 수정 모델
    """
