"""
피드의 프로필 관련 API
"""
from typing import List

from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(
    prefix="/profiles",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


class UserProfile(BaseModel):
    """
    User profile 모델
    """
    user_id: str


class VisitorProfile(BaseModel):
    """
    Visitor profile 모델
    """
    user_id: str


@router.get("/{user_id}", response_model=UserProfile)
async def get_profile(user_id: str):
    """
    특정 유저 프로필 정보 조회 API
    :param user_id:
    :return: user profile
    """
    print(user_id)
    return None


@router.put("", response_model="")
async def update_profile(profile: UserProfile, token: str):
    """
    본인 프로필 수정 API
    :param profile: 업데이트 할 profile
    :param token: auth 확인용
    :return:
    """
    print(profile, token)
    return {"message": "Profile updated"}


@router.get("/visitors", response_model=List[VisitorProfile])
async def get_visitors(token: str):
    """
    방문자 리스트 API
    :param token:
    :return:
    """
    print(token)
    return None
