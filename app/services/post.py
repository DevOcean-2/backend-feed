"""
게시물 서비스 로직
"""
from datetime import datetime, UTC
from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, cast, Integer, String
import boto3, base64, io, os, uuid
from dotenv import load_dotenv
load_dotenv()

from app.schemas.post import PostResponse, Like, PostCreate, PostUpdate
from app.models.post import Post as PostTable
from app.models.post import Like as LikeTable
from app.models.post import User as UserTable
from app.models.post import UserAbstractProfile
from app.models.notification import Notification as NotiTable
from app.utils.parser import extract_hashtags

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

def famous_posts(db: Session) -> List[PostResponse]:
    """
    좋아요 수 기준 상위 5개의 인기 게시물 반환 (사용자 이름 포함)
    """
    posts = (
        db.query(
            PostTable,
            UserTable.name.label('user_name'),
            func.count(LikeTable.post_id).label('like_count')
        )
        .join(
            UserTable, 
            PostTable.user_id == cast(UserTable.social_id, String)  # Integer 대신 users.id를 String으로 캐스팅
        )
        .outerjoin(LikeTable, PostTable.id == LikeTable.post_id)
        .group_by(PostTable.id, UserTable.name)
        .order_by(desc('like_count'))
        .limit(5)
        .all()
    )
    
    post_list = []
    for post, user_name, like_count in posts:  # user_name 추가
        likes = list_post_likes(post.id, db)
        post_list.append({
            "post_id" : post.id,
            "user_id" : post.user_id,
            "user_name" : user_name,
            "image_urls" : post.image_urls,
            "liked_by" : likes
        })
    
    return post_list

def create_post(user_id: str, db: Session, post_create: PostCreate) -> PostResponse:
    """
    새 게시물 생성 로직
    """
    try:
        # base64 이미지들을 S3에 업로드
        s3_urls = []
        for base64_image in post_create.image_urls:
            s3_url = upload_image_to_s3(base64_image)
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
        raise HTTPException(status_code=500, detail=str(e))

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
        # S3에서 이미지들 삭제
        s3_client = create_s3_client()
        for image_url in post.image_urls:
            try:
                key = image_url.split('.com/')[-1]
                s3_client.delete_object(Bucket='balm-bucket', Key=key)
            except Exception as e:
                print(f"Failed to delete S3 image: {str(e)}")

        # DB에서 게시물 삭제
        db.delete(post)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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

def toggle_post_like(post_id: int, user_id: str, db: Session) -> dict:
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
            return {
                "message": "Successfully unliked a post",
                "is_liked": False,
                "likes_count": get_post_likes_count(post_id, db)
            }
        
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
        
        return {
            "message": "Successfully liked a post",
            "is_liked": True,
            "likes_count": get_post_likes_count(post_id, db)
        }

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
        like_responses.append({
            "user_id" : like.user_id,
            "nickname" : like.dog_name,
            "profile_image_url" : like.photo_path
        })

    return like_responses

def create_s3_client():
    """S3 클라이언트 생성"""
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name='ap-northeast-2'
    )

def upload_image_to_s3(base64_string: str) -> str:
    """
    Base64 이미지를 S3에 업로드하고 URL 반환
    """
    try:
        s3_client = create_s3_client()
        bucket_name = 'balm-bucket'

        # base64 디코딩
        if 'base64,' in base64_string:
            image_data = base64_string.split('base64,')[1]
        else:
            image_data = base64_string
            
        image_bytes = base64.b64decode(image_data)
        
        # S3에 업로드
        file_id = str(uuid.uuid4())
        key = f"images/feed/{file_id}.jpg"
        
        s3_client.upload_fileobj(
            io.BytesIO(image_bytes),
            bucket_name,
            key,
            ExtraArgs={
                'ContentType': 'image/jpeg',
                'CacheControl': 'max-age=31536000'
            }
        )
        
        return f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{key}"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")