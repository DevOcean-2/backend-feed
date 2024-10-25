"""
게시물 데이터베이스 모델
"""
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.database.db import Base


class Post(Base):
    """
    Post 테이블 모델
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    content = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.now(UTC))
    image_urls = Column(JSONB)
    hashtags = Column(JSONB)

    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")


class Like(Base):
    """
    Like 테이블 모델
    """
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), index=True)
    user_id = Column(String, index=True)
    nickname = Column(String)
    user_image_url = Column(String, nullable=True)

    post = relationship("Post", back_populates="likes")
