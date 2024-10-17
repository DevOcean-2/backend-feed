"""
피드의 알림 관련 API
"""
from typing import List
from fastapi import APIRouter

from app.schemas import notification as noti_schema

router = APIRouter(
    prefix="/notifications",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[noti_schema.Notification])
async def get_notifications(token: str):
    """
    전체 알림 리스트
    :param token:
    :return:
    """
    print(token)
    return None


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str, token: str):
    """
    특정 알림 삭제
    :param notification_id:
    :param token:
    :return:
    """
    print(notification_id, token)
    return {"message": "Successfully deleted a notification"}


@router.delete("")
async def delete_all_notifications(token: str):
    """
    전체 알림 삭제
    :param token:
    :return:
    """
    print(token)
    return {"message": "Successfully deleted all notifications"}
