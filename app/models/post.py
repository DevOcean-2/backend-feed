"""
게시물 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.database.db import Base


class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    content = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.now(UTC))
    image_urls = Column(JSONB)
    likes = relationship("Like", back_populates="post")


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), index=True)
    user_id = Column(String, index=True)
    user_image_url = Column(String, nullable=True)

    post = relationship("Post", back_populates="likes")
