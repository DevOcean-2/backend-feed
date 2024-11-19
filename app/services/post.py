"""
게시물 서비스 로직
"""
from datetime import datetime, UTC
from random import sample
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, cast, String
from fastapi import HTTPException

from app.schemas.post import PostResponse, FamousResponse, Like, LikeToggle, PostCreate, PostUpdate
from app.models.post import Post as PostTable
from app.models.post import Like as LikeTable
from app.models.post import User as UserTable
from app.models.post import UserAbstractProfile
from app.models.notification import Notification as NotiTable
from app.utils.parser import extract_hashtags
from app.utils.image import upload_image_to_s3, create_s3_client

def list_posts(user_id: str, db: Session) -> List[PostResponse]:
    """
    유저 포스트 리스팅 로직
    """
    # 유저 id 기반으로 게시물 db 긁어오기
    posts: List[PostTable] = db.query(PostTable).filter(PostTable.user_id == user_id).all()
    post_list = []
    for post in posts:
        likes = list_post_likes(post.id, db)
        post_list.append(PostResponse(
            post_id=post.id,
            user_id=post.user_id,
            image_urls=post.image_urls,  # S3 URL 리스트
            content=post.content,
            uploaded_at=post.uploaded_at,
            liked_by=likes,
        ))
    return post_list

def famous_posts(db: Session) -> List[FamousResponse]:
    """
    좋아요 수 기준 상위 5개의 인기 게시물 반환 (사용자 이름 포함)
    """
    posts = (
        db.query(
            PostTable,
            UserTable.name.label('user_name'),
            # pylint: disable=not-callable # SQLAlchemy 2.0.0 이후로 업그레이드된 이후 발생하는 pylint의 문제라고 합니다
            func.count(LikeTable.post_id).label('like_count')
        )
        .join(
            UserTable, PostTable.user_id == cast(UserTable.social_id, String)
        )
        .outerjoin(LikeTable, PostTable.id == LikeTable.post_id)
        .group_by(PostTable.id, UserTable.name)
        .order_by(desc('like_count'))
        .limit(100) # 상위 100개를 가져오고
        .all()
    )
    random_posts = sample(posts, min(5, len(posts))) # 5개를 랜덤하게 추출

    post_list = []
    for post, user_name, _ in random_posts:  # user_name 추가
        likes = list_post_likes(post.id, db)
        post_list.append(FamousResponse(
            post_id=post.id,
            user_id=post.user_id,
            user_name=user_name,
            image_urls=post.image_urls,
            liked_by=likes
        ))
    return post_list

def create_post(user_id: str, db: Session, post_create: PostCreate) -> PostResponse:
    """
    새 게시물 생성 로직
    """
    try:
        # base64 이미지들을 S3에 업로드
        s3_urls = []
        for base64_image in post_create.image_urls:
            s3_client = create_s3_client()
            s3_url = upload_image_to_s3(base64_image, s3_client)
            s3_urls.append(s3_url)

        # 해시태그 추출 및 게시물 생성
        hashtags = extract_hashtags(post_create.content)
        post = PostTable(
            user_id=user_id,
            content=post_create.content,
            uploaded_at=datetime.now(),
            image_urls=s3_urls,  # S3 URL 리스트 저장
            hashtags=hashtags
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        likes = list_post_likes(post.id, db)

        return PostResponse(
            post_id=post.id,
            user_id=post.user_id,
            image_urls=post.image_urls,
            content=post.content,
            uploaded_at=post.uploaded_at,
            liked_by=likes,
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e

def update_post(user_id: str, post_id: int, db: Session, post_update: PostUpdate) -> PostResponse:
    """
    게시물 내용 수정 로직
    """
    post: PostTable = db.query(PostTable).filter(PostTable.id == post_id).first()
    if user_id != post.user_id:
        raise HTTPException(status_code=403, detail="Forbidden user")

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    hashtags = extract_hashtags(post_update.content)
    post.content = post_update.content
    post.hashtags = hashtags
    try:
        db.commit()
        db.refresh(post)
    except IntegrityError:
        db.rollback()
        raise

    likes = list_post_likes(post.id, db)

    return PostResponse(
        post_id=post.id,
        user_id=post.user_id,
        image_urls=post.image_urls,
        content=post.content,
        uploaded_at=post.uploaded_at,
        liked_by=likes,
    )


def delete_post(user_id: str, post_id: int, db: Session) -> None:
    """게시물 삭제 로직"""
    post = db.query(PostTable).filter(PostTable.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if user_id != post.user_id:
        raise HTTPException(status_code=403, detail="Forbidden user")

    try:
        db.delete(post) # DB에서 먼저 삭제 시도
        # S3 이미지 삭제 시도
        s3_client = create_s3_client()
        for image_url in post.image_urls:
            try:
                key = image_url.split('.com/')[-1]
                s3_client.delete_object(Bucket='balm-bucket', Key=key)
            except Exception as e:
                db.rollback() # 이미지 삭제 실패시 DB 롤백
                raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}") from e
        db.commit() # 모든 작업 성공시 커밋

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e

def list_posts_with_hashtag(hashtag: str, db: Session) -> List[PostResponse]:
    posts: List[PostTable] = db.query(PostTable).filter(PostTable.hashtags.contains([hashtag])).all()

    post_list = []
    for post in posts:
        # 게시물 좋아요 리스트 긁어오기
        likes = list_post_likes(post.id, db)

        # 리스폰스 생성
        post_list.append(PostResponse(
            post_id=post.id,
            user_id=post.user_id,
            image_urls=post.image_urls,
            content=post.content,
            uploaded_at=post.uploaded_at,
            liked_by=likes,
        ))

    return post_list

def get_post_likes_count(post_id: int, db: Session) -> int:
    return db.query(LikeTable).filter(LikeTable.post_id == post_id).count()

def toggle_post_like(post_id: int, user_id: str, db: Session) -> LikeToggle:
    """
    게시물 좋아요 토글 로직
    """
    post: PostTable = db.query(PostTable).filter(PostTable.id == post_id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = (db.query(LikeTable).filter(
        LikeTable.post_id == post_id,
        LikeTable.user_id == user_id
    ).first())

    try:
        if existing_like:
            # 좋아요가 있으면 좋아요와 알림 삭제
            notification = db.query(NotiTable).filter(NotiTable.like_id == existing_like.id).first()
            if notification:
                db.delete(notification)
            db.delete(existing_like)
            db.commit()
            return LikeToggle(
                message="Successfully unliked a post",
                is_liked=False,
                likes_count=get_post_likes_count(post_id, db)
            )
        # 좋아요가 없으면 좋아요와 알림 추가
        like = LikeTable(
            post_id=post_id,
            user_id=user_id,
        )
        db.add(like)
        db.commit()
        db.refresh(like)

        notification = NotiTable(
            user_id=post.user_id,
            is_read=False,
            created_at=datetime.now(UTC),
            post_id=post_id,
            like_id=like.id
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        return LikeToggle(
            message="Successfully liked a post",
            is_liked=True,
            likes_count=get_post_likes_count(post_id, db)
        )
    except IntegrityError:
        db.rollback()
        raise

def list_post_likes(post_id: int, db: Session) -> List[Like]:
    """
    게시물의 좋아요 리스팅
    """
    likes = (
        db.query(
            LikeTable.user_id,
            UserAbstractProfile.dog_name,
            UserAbstractProfile.photo_path
        )
        .join(
            UserAbstractProfile,
            LikeTable.user_id == UserAbstractProfile.social_id
        )
        .filter(LikeTable.post_id == post_id)
        .all()
    )
    like_responses = []
    for like in likes:
        like_responses.append(Like(
            user_id=like.user_id,
            nickname=like.dog_name,
            profile_image_url=like.photo_path
        ))
    return like_responses
