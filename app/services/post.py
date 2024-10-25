"""
게시물 서비스 로직
"""
from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas.post import PostResponse, Like, PostCreate, PostUpdate
from app.models.post import Post as PostTable
from app.models.post import Like as LikeTable
from app.utils.parser import extract_hashtags


def list_posts(user_id: str, db: Session) -> List[PostResponse]:
    """
    유저 포스트 리스팅 로직
    """
    # 유저 id 기반으로 게시물 db 긁어오기
    posts: List[PostTable] = db.query(PostTable).filter(PostTable.user_id == user_id).all()
    post_list = []
    for post in posts:
        # 게시물 좋아요 리스트 긁어오기
        likes = list_post_likes(post.id, db)

        # 리스폰스 생성
        post_list.append(PostResponse(
            post_id=post.id,
            image_urls=post.image_urls,
            content=post.content,
            uploaded_at=post.uploaded_at,
            liked_by=likes,
        ))

    return post_list


def create_post(user_id: str, db: Session, post_create: PostCreate) -> PostResponse:
    """
    새 게시물 생성 로직
    """
    hashtags = extract_hashtags(post_create.content)
    post = PostTable(
        user_id=user_id,
        content=post_create.content,
        uploaded_at=datetime.now(),
        image_urls=post_create.image_urls,
        hashtags=hashtags
    )

    db.add(post)
    try:
        db.commit()
        db.refresh(post)
    except IntegrityError:
        db.rollback()
        raise

    likes = list_post_likes(post.id, db)

    return PostResponse(
        post_id=post.id,
        image_urls=post.image_urls,
        content=post.content,
        uploaded_at=post.uploaded_at,
        liked_by=likes,
    )


def update_post(user_id: str, post_id: int, db: Session, post_update: PostUpdate) -> PostResponse:
    """
    게시물 내용 수정 로직
    """
    post: PostTable = db.query(PostTable).filter(PostTable.id == post_id).first()
    if user_id != post.user_id:
        raise HTTPException(status_code=403, detail="Forbidden user")

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    post.content = post_update.content
    try:
        db.commit()
        db.refresh(post)
    except IntegrityError:
        db.rollback()
        raise

    likes = list_post_likes(post.id, db)

    return PostResponse(
        post_id=post.id,
        image_urls=post.image_urls,
        content=post.content,
        uploaded_at=post.uploaded_at,
        liked_by=likes,
    )


def delete_post(user_id: str, post_id: int, db: Session) -> None:
    """
    게시물 삭제 로직
    """
    post = db.query(PostTable).filter(PostTable.id == post_id).first()
    if user_id != post.user_id:
        raise HTTPException(status_code=403, detail="Forbidden user")

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()


def like_post(post_id: int, db: Session, like_create: Like) -> None:
    """
    게시물 좋아요 로직
    """
    post = db.query(PostTable).filter(PostTable.id == post_id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = (db.query(LikeTable).filter(LikeTable.post_id == post_id,
                                                LikeTable.user_id == like_create.user_id).first())

    if existing_like:
        raise HTTPException(status_code=400, detail="Like conflict")

    like = LikeTable(
        post_id=post_id,
        user_id=like_create.user_id,
        nickname=like_create.nickname,
        user_image_url=like_create.profile_image_url
    )
    try:
        db.commit()
        db.refresh(like)
    except IntegrityError:
        db.rollback()
        raise


def unlike_post(post_id: int, user_id: str, db: Session) -> None:
    """
    게시물 좋아요 취소 로직
    """
    post = db.query(PostTable).filter(PostTable.id == post_id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    like = (db.query(LikeTable).
            filter(LikeTable.post_id == post_id, LikeTable.user_id == user_id).first())

    if like is None:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()


def list_post_likes(post_id: int, db: Session) -> List[Like]:
    """
    게시물의 좋아요 리스팅
    """
    likes: List[LikeTable] = db.query(LikeTable).filter(LikeTable.post_id == post_id).all()
    like_responses = []
    for like in likes:
        like_responses.append(Like(
            user_id=like.user_id,
            nickname=like.nickname,
            profile_image_url=like.user_image_url
        ))

    return like_responses
