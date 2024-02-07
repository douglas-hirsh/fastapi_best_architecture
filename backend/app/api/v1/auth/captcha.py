#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fast_captcha import img_captcha
from fastapi import APIRouter, Depends, Request
from fastapi_limiter.depends import RateLimiter
from starlette.concurrency import run_in_threadpool

from backend.app.common.redis import redis_client
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.core.conf import settings

router = APIRouter()


@router.get(
    '/captcha',
    summary='Obtain login verification code.',
    dependencies=[Depends(RateLimiter(times=5, seconds=10))],
)
async def get_captcha(request: Request) -> ResponseModel:
    """
    Possible performance loss may exist in this interface.,Although it is an asynchronous interface,However, the verification code generation is.IOIntensive task.,Use thread pool to minimize performance loss
    """
    img_type: str = 'base64'
    img, code = await run_in_threadpool(img_captcha, img_byte=img_type)
    ip = request.state.ip
    await redis_client.set(
        f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{ip}', code, ex=settings.CAPTCHA_LOGIN_EXPIRE_SECONDS
    )
    return await response_base.success(data={'image_type': img_type, 'image': img})
