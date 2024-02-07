#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.models.base import MappedBase


def create_engine_and_session(url: str | URL):
    try:
        # Database engine
        engine = create_async_engine(url, echo=settings.DB_ECHO, future=True, pool_pre_ping=True)
        # log.success('Database connection successful')
    except Exception as e:
        log.error('❌ Database connection failed {}', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session


SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:'
    f'{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'
)

async_engine, async_db_session = create_engine_and_session(SQLALCHEMY_DATABASE_URL)


async def get_db() -> AsyncSession:
    """session Generator"""
    session = async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()


# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]


async def create_table():
    """Create database table."""
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


def uuid4_str() -> str:
    """Database engine UUID Type compatibility solution"""
    return str(uuid4())
