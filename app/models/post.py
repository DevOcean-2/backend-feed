"""
게시물 데이터베이스 모델
"""
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
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
    # nickname = Column(String)
    # profile_image_url = Column(String, nullable=True)

    post = relationship("Post", back_populates="likes")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # email = Column(String, unique=True, index=True)
    name = Column(String)
    social_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

class UserAbstractProfile(Base):
    __tablename__ = "users_profile"
    id = Column(Integer, primary_key=True, index=True)
    social_id = Column(String, ForeignKey("users.social_id"), unique=True)  # social_id로 외래키 설정
    dog_name = Column(String) # 이름
    photo_path = Column(String) # 사진 경로