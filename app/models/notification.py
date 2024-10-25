"""
알림 데이터베이스 모델
"""
from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

from app.database.db import Base


class Notification(Base):
    """
    알림 테이블 모델
    """
    __tablename__ = 'feed_notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))

    post_id = Column(Integer, ForeignKey('posts.id'))
    like_id = Column(Integer, ForeignKey('likes.id'))
