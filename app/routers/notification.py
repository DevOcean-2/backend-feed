"""
피드의 알림 관련 API
"""
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/notifications",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


class Notification(BaseModel):
    """
    알림 모델
    """
    message: str
    timestamp: str


@router.get("", response_model=List[Notification])
async def get_notifications(token: str):
    """
    전체 알림 리스트
    :param token:
    :return:
    """
    print(token)
    return None


@router.delete("/{notification_id}", response_model="")
async def delete_notification(notification_id: str, token: str):
    """
    특정 알림 삭제
    :param notification_id:
    :return:
    """
    print(notification_id, token)
    return {"message": "Successfully deleted a notification"}


@router.delete("", response_model="")
async def delete_all_notifications(token: str):
    """
    전체 알림 삭제
    :param token:
    :return:
    """
    print(token)
    return {"message": "Successfully deleted all notifications"}
