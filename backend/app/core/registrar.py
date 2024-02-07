#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from starlette.middleware.authentication import AuthenticationMiddleware

from backend.app.api.routers import v1
from backend.app.common.exception.exception_handler import register_exception
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.database.db_mysql import create_table
from backend.app.middleware.jwt_auth_middleware import JwtAuthMiddleware
from backend.app.middleware.opera_log_middleware import OperaLogMiddleware
from backend.app.utils.demo_site import demo_site
from backend.app.utils.health_check import ensure_unique_route_names, http_limit_callback
from backend.app.utils.openapi import simplify_operation_ids
from backend.app.utils.serializers import MsgSpecJSONResponse


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    Start initialization

    :return:
    """
    # Create database table.
    await create_table()
    # Connection redis
    await redis_client.open()
    # Initialize limiter
    await FastAPILimiter.init(redis_client, prefix=settings.LIMITER_REDIS_PREFIX, http_callback=http_limit_callback)

    yield

    # Close redis Connection
    await redis_client.close()
    # Close limiter
    await FastAPILimiter.close()


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        lifespan=register_init,
    )

    # Static file
    register_static_file(app)

    # middleware
    register_middleware(app)

    # route
    register_router(app)

    # pagination
    register_page(app)

    # Global exception handling
    register_exception(app)

    return app


def register_static_file(app: FastAPI):
    """
    Static fileDevelop interactive mode, Production use nginx Static resource service

    :param app:
    :return:
    """
    if settings.STATIC_FILES:
        import os

        from fastapi.staticfiles import StaticFiles

        if not os.path.exists('./static'):
            os.mkdir('./static')
        app.mount('/static', StaticFiles(directory='static'), name='static')


def register_middleware(app: FastAPI):
    """
    middleware,Execution order from bottom to top

    :param app:
    :return:
    """
    # Gzip: Always at the top
    if settings.MIDDLEWARE_GZIP:
        from fastapi.middleware.gzip import GZipMiddleware

        app.add_middleware(GZipMiddleware)
    # Opera log
    app.add_middleware(OperaLogMiddleware)
    # JWT auth, required
    app.add_middleware(
        AuthenticationMiddleware, backend=JwtAuthMiddleware(), on_error=JwtAuthMiddleware.auth_exception_handler
    )
    # Access log
    if settings.MIDDLEWARE_ACCESS:
        from backend.app.middleware.access_middleware import AccessMiddleware

        app.add_middleware(AccessMiddleware)
    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    """
    route

    :param app: FastAPI
    :return:
    """
    dependencies = [Depends(demo_site)] if settings.DEMO_MODE else None

    # API
    app.include_router(v1, dependencies=dependencies)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)


def register_page(app: FastAPI):
    """
    paginationInquiry

    :param app:
    :return:
    """
    add_pagination(app)
