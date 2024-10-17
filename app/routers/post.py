"""
피드의 포스팅 관련 API
"""
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/posts",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


class Post(BaseModel):
    """
    게시물 모델
    """
    post_id: int
    user_id: int
    content: str
    likes: int = 0


@router.get("", response_model=List[Post])
async def list_posts(user_id: str):
    """
    특정 유저의 전체 게시물 리스팅 API
    :param user_id:
    :return:
    """
    print(user_id)
    return None


@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int):
    """
    특정 게시물 상세 조회 API
    :param post_id:
    :return:
    """
    print(post_id)
    return None


@router.post("", response_model="")
async def create_post(post: Post, token: str):
    """
    게시물 생성 API
    :param post:
    :param token:
    :return:
    """
    print(post, token)
    return {"message": "Successfully created a post"}


@router.put("/{post_id}", response_model="")
async def update_post(post: Post, token: str):
    """
    본인 게시물 수정 API
    :param post:
    :param token:
    :return:
    """
    print(post, token)
    return {"message": "Successfully updated a post"}


@router.post("/{post_id}/like", response_model="")
async def like_post(post_id: int):
    """
    게시물 좋아요 API
    :param post_id:
    :return:
    """
    print(post_id)
    return {"message": "Successfully liked a post"}


@router.delete("/{post_id}", response_model="")
async def delete_post(post_id: int, token: str):
    """
    게시물 삭제 API
    :param post_id:
    :param token:
    :return:
    """
    print(post_id, token)
    return {"message": "Successfully deleted a post"}
