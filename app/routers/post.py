"""
피드의 포스팅 관련 API
"""
from typing import List
from fastapi import APIRouter

from app.schemas import post as post_schema

router = APIRouter(
    prefix="/posts",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[post_schema.PostResponse])
async def list_posts(user_id: str):
    """
    특정 유저의 전체 게시물 리스팅 API
    :param user_id:
    :return:
    """
    print(user_id)
    return None


@router.get("/{post_id}", response_model=post_schema.PostResponse)
async def get_post(post_id: int):
    """
    특정 게시물 상세 조회 API
    :param post_id:
    :return:
    """
    print(post_id)
    return None


@router.post("")
async def create_post(post: post_schema.PostCreate, token: str):
    """
    게시물 생성 API
    :param post:
    :param token:
    :return:
    """
    print(post, token)
    return {"message": "Successfully created a post"}


@router.put("/{post_id}")
async def update_post(post: post_schema.PostUpdate, token: str):
    """
    본인 게시물 수정 API
    :param post:
    :param token:
    :return:
    """
    print(post, token)
    return {"message": "Successfully updated a post"}


@router.post("/{post_id}/like")
async def like_post(post_id: int):
    """
    게시물 좋아요 API
    :param post_id:
    :return:
    """
    print(post_id)
    return {"message": "Successfully liked a post"}


@router.delete("/{post_id}")
async def delete_post(post_id: int, token: str):
    """
    게시물 삭제 API
    :param post_id:
    :param token:
    :return:
    """
    print(post_id, token)
    return {"message": "Successfully deleted a post"}
