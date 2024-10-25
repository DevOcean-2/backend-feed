"""
토큰 관련 util 함수
"""
import os
from datetime import datetime, UTC, timedelta

import jwt
from fastapi import HTTPException, Depends
from fastapi_jwt_auth import AuthJWT


def get_social_id(token: AuthJWT = Depends()) -> str:
    """
    토큰 까서 소셜 id 가져오기
    """
    try:
        token.jwt_required()
        claims = token.get_raw_jwt()
        social_id = claims.get("social_id")
        if social_id is None:
            raise HTTPException(status_code=401, detail="Missing social_id")
        return social_id
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from exc


def create_jwt_access_token(user_id: str) -> str:
    """
    JWT 토큰 생성
    """
    payload = {
        "sub": user_id,
        "social_id": user_id,
        "exp": datetime.now(UTC) + timedelta(minutes=int(os.getenv("JWT_EXPIRATION_DELTA"))),
        "type": "access"
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

    return token.decode('utf-8') if isinstance(token, bytes) else token
