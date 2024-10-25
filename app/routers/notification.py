"""
피드의 알림 관련 API
"""
from typing import List
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import notification as noti_schema
from app.services import notification as noti_service
from app.utils.token import get_social_id

router = APIRouter(
    prefix="/notifications",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[noti_schema.NotiResponse])
async def get_notifications(token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    전체 알림 리스트
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)

    return noti_service.get_notifications(user_id, db)


@router.put("/{post_id}/read")
async def mark_notification_as_read(post_id: int, token: AuthJWT = Depends(),
                                    db: Session = Depends(get_db)):
    """
    특정 알림을 읽음 상태로 변경
    :param post_id:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)

    noti_service.mark_notification_as_read(post_id, user_id, db)

    return {"message": "A notification marked as read"}
