"""
피드의 포스팅 관련 API
"""
from typing import List
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.post import PostResponse, PostCreate, PostUpdate, Like
from app.services import post as post_service
from app.utils.token import get_social_id

router = APIRouter(
    prefix="/posts",
    tags=["Feed"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[PostResponse])
async def list_posts(user_id: str, token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    특정 유저의 전체 게시물 리스팅 API
    :param user_id:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()

    return post_service.list_posts(user_id, db)


@router.get("/hashtag/{hashtag}", response_model=List[PostResponse])
async def list_posts_with_hashtag(hashtag: str, token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    해시태그 게시물 리스팅 API
    :param hashtag:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()

    return post_service.list_posts_with_hashtag(hashtag, db)


@router.post("", response_model=PostResponse)
async def create_post(post: PostCreate,
                      token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    게시물 생성 API
    :param post:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)

    return post_service.create_post(user_id, db, post)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post: PostUpdate,
                      token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    본인 게시물 수정 API
    :param post_id:
    :param post:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)

    return post_service.update_post(user_id, post_id, db, post)


@router.delete("/{post_id}")
async def delete_post(post_id: int, token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    게시물 삭제 API
    :param post_id:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)
    post_service.delete_post(user_id, post_id, db)

    return {"message": "Successfully deleted a post"}


@router.post("/{post_id}/likes")
async def like_post(post_id: int, like: Like,
                    token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    게시물 좋아요 API
    :param post_id:
    :param like:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    post_service.like_post(post_id, db, like)

    return {"message": "Successfully liked a post"}


@router.delete("/{post_id}/likes")
async def unlike_post(post_id: int, token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    게시물 좋아요 취소 API
    :param post_id:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)
    post_service.unlike_post(post_id, user_id, db)

    return {"message": "Successfully unliked a post"}
