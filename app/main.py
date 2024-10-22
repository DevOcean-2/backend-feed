"""
main.py
"""

import logging
import os
import uuid
from fastapi import FastAPI, APIRouter
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from starlette.responses import Response

from app.database import db
from app.routers import post, notification

logger = logging.getLogger(__name__)


class Settings(BaseModel):
    """
    AuthJWT config setting
    """
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY")


@AuthJWT.load_config
def get_config():
    """
    AuthJWT config
    """
    return Settings()


# 테이블 생성 (만들 때 모델 import 하고 해야함)
db.Base.metadata.create_all(bind=db.engine)

# fastAPI app 생성
app = FastAPI(
    title="Balbalm Feed Backend",
    description="backend for balbalm feed service",
    version="1.0-beta",
    openapi_url="/openapi.json",
)

app.logger = logger


@app.middleware("http")
async def http_log(request, call_next):
    """
    로그
    :param request:
    :param call_next:
    :return:
    """
    response = await call_next(request)
    response_body = b''
    log_uuid = str(uuid.uuid1())[:8]

    async for chunk in response.body_iterator:
        response_body += chunk
    logger.info("Log ID : %s - Request URL : %s %s",
                log_uuid, str(request.method), str(request.url))
    if "request_body" in context:
        logger.info("Log ID : %s - Request Body : %s", log_uuid, context["request_body"])
    logger.info("Log ID : %s - Response Body : %s", log_uuid, response_body)
    logger.info("Log ID : %s - Response Status Code : %s", log_uuid, str(response.status_code))

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )

app.add_middleware(ContextMiddleware)

# feed prefix 추가
feed_router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)

# feed router 에 상세 path 추가
feed_router.include_router(post.router)
feed_router.include_router(notification.router)

# app 에 추가
app.include_router(feed_router)
