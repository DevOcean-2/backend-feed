"""
알림 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from app.schemas.notification import NotiType
from app.database.db import Base


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    noti_type = Column(Enum(NotiType), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    mission_id = Column(Integer, nullable=True)
    like_id = Column(Integer, ForeignKey('likes.id'), nullable=True)

    likes = relationship("Like", back_populates="notifications")
