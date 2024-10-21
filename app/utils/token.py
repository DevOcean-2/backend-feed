"""
토큰 관련 util 함수
"""
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
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from exc
