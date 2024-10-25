"""
models
"""
from sqlalchemy.orm import relationship

from app.models.post import Post, Like
from app.models.notification import Notification

Post.noti = relationship("Notification", back_populates="post", cascade="all, delete-orphan")
Like.noti = relationship("Notification", back_populates="like", cascade="all, delete-orphan")

Notification.post = relationship('Post', back_populates='noti')
Notification.like = relationship("Like", back_populates="noti")
