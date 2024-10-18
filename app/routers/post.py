"""
피드의 포스팅 관련 API
"""
from typing import List
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import post as post_schema

router = APIRouter(
    prefix="/posts",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[post_schema.PostResponse])
async def list_posts(user_id: str, token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    특정 유저의 전체 게시물 리스팅 API
    :param user_id:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    print(user_id, db)
    return None


@router.post("")
async def create_post(post: post_schema.PostCreate, token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    게시물 생성 API
    :param post:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    print(post, db)
    return {"message": "Successfully created a post"}


@router.put("/{post_id}")
async def update_post(post: post_schema.PostUpdate, token: AuthJWT = Depends()):
    """
    본인 게시물 수정 API
    :param post:
    :param token:
    :return:
    """
    token.jwt_required()
    print(post)
    return {"message": "Successfully updated a post"}


@router.delete("/{post_id}")
async def delete_post(post_id: int, token: AuthJWT = Depends()):
    """
    게시물 삭제 API
    :param post_id:
    :param token:
    :return:
    """
    token.jwt_required()
    print(post_id)
    return {"message": "Successfully deleted a post"}


@router.post("/{post_id}/likes")
async def like_post(post_id: int, token: AuthJWT = Depends()):
    """
    게시물 좋아요 API
    :param post_id:
    :param token:
    :return:
    """
    token.jwt_required()
    print(post_id)
    return {"message": "Successfully liked a post"}


@router.delete("/{post_id}/likes")
async def unlike_post(post_id: int, token: AuthJWT = Depends()):
    """
    게시물 좋아요 취소 API
    :param post_id:
    :param token:
    :return:
    """
    token.jwt_required()
    print(post_id)
    return {"message": "Successfully unliked a post"}
