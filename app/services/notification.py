"""
알림 서비스
"""
from collections import defaultdict
from datetime import datetime
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.notification import Notification as NotiTable
from app.models.post import Like as LikeTable
from app.models.post import UserAbstractProfile
from app.schemas.notification import NotiResponse
from app.schemas.post import Like


def get_notifications(user_id: str, db: Session) -> List[NotiResponse]:
    """
    전체 알림 리스트 조회
    """
    notifications: List[NotiTable] = db.query(NotiTable).filter(NotiTable.user_id == user_id).all()

    post_notifications = defaultdict(list)
    for notification in notifications:
        post_notifications[notification.post_id].append(notification)

    noti_response: List[NotiResponse] = []
    for post_id, notifications in post_notifications.items():
        likes: List[Like] = []
        is_read: bool = True
        created_at_list: List[datetime] = []

        for notification in notifications:
            like: LikeTable = (
                db.query(
                    LikeTable.user_id,
                    UserAbstractProfile.dog_name.label('nickname'),   # 피드홈에 등록한 닉네임
                    UserAbstractProfile.photo_path.label('profile_image_url'), # 피드홈에 등록한 프로필 이미지
                )
                .join(
                    UserAbstractProfile,
                    LikeTable.user_id == UserAbstractProfile.social_id
                )
                .filter(
                    LikeTable.id == notification.like_id
                ).first()
            )
            likes.append(Like(
                user_id=like.user_id,
                nickname=like.nickname,
                profile_image_url=like.profile_image_url
            ))
            if not notification.is_read:
                is_read = False
            created_at_list.append(notification.created_at)
        noti_response.append(NotiResponse(
            is_read=is_read,
            created_at=max(created_at_list),
            post_id=post_id,
            likes=likes
        ))

    return noti_response


def mark_notification_as_read(post_id: int, user_id: str, db: Session) -> None:
    """
    특정 알림을 읽음 상태로 변경
    """
    notifications: List[NotiTable] = (db.query(NotiTable).
                                      filter(NotiTable.post_id == post_id,
                                             NotiTable.user_id == user_id).all())
    for notification in notifications:
        notification.is_read = True

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
