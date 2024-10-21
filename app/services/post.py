"""
게시물 서비스 로직
"""
from datetime import datetime
from typing import List

from pydantic import HttpUrl, ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas.post import PostResponse, Like, PostCreate
from app.models.post import Post as PostTable
from app.models.post import Like as LikeTable


def list_user_posts(user_id: str, db: Session) -> List[PostResponse]:
    """
    유저 포스트 리스팅 로직
    """
    # 유저 id 기반으로 게시물 db 긁어오기
    posts: List[PostTable] = db.query(PostTable).filter(PostTable.user_id == user_id).all()
    post_list = []
    for post in posts:
        # url 파싱
        try:
            image_urls = [HttpUrl(url) for url in post.image_urls]  # 유효성 검사와 변환
        except ValidationError:
            image_urls = []
        # 게시물 좋아요 리스트 긁어오기
        likes: List[LikeTable] = db.query(LikeTable).filter(LikeTable.post_id == post.id).all()
        like_responses = []
        for like in likes:
            like_responses.append(Like(
                user_id=like.user_id,
                nickname=like.nickname,
                profile_image_url=like.user_image_url
            ))
        # 리스폰스 생성
        post_list.append(PostResponse(
            post_id=post.id,
            image_urls=image_urls,
            content=post.content,
            uploaded_at=post.uploaded_at,
            liked_by=like_responses,
        ))

    return post_list


def create_new_post(user_id: str, db: Session, post_create: PostCreate) -> PostResponse:
    """
    새 게시물 생성 로직
    """
    post = PostTable(
        user_id=user_id,
        content=post_create.content,
        uploaded_at=datetime.now(),
        image_urls=post_create.image_url
    )

    db.add(post)
    try:
        db.commit()
        db.refresh(post)
    except IntegrityError:
        db.rollback()
        raise

    return PostResponse().from_orm(post)
