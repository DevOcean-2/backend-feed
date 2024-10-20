"""
피드의 알림 관련 API
"""
from typing import List
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.schemas import notification as noti_schema

router = APIRouter(
    prefix="/notifications",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[noti_schema.Notification])
async def get_notifications(token: AuthJWT = Depends()):
    """
    전체 알림 리스트
    :param token:
    :return:
    """
    token.jwt_required()

    return None


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str, token: AuthJWT = Depends()):
    """
    특정 알림 삭제
    :param notification_id:
    :param token:
    :return:
    """
    token.jwt_required()
    print(notification_id)

    return {"message": "Successfully deleted a notification"}


@router.delete("")
async def delete_all_notifications(token: AuthJWT = Depends()):
    """
    전체 알림 삭제
    :param token:
    :return:
    """
    token.jwt_required()

    return {"message": "Successfully deleted all notifications"}


@router.put("/{notification_id}/read")
async def mark_notification_as_read(notification_id: str, token: AuthJWT = Depends()):
    """
    특정 알림을 읽음 상태로 변경
    :param notification_id:
    :param token:
    :return:
    """
    token.jwt_required()
    print(notification_id)

    return {"message": "A notification marked as read"}


@router.put("/read_all")
async def mark_all_notifications_as_read(token: AuthJWT = Depends()):
    """
    전체 알림을 읽음 상태로 변경
    :param token:
    :return:
    """
    token.jwt_required()

    return {"message": "All notifications marked as read"}
