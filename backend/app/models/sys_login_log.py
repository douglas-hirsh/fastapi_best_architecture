#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import DataClassBase, id_key
from backend.app.utils.timezone import timezone


class LoginLog(DataClassBase):
    """Login log table"""

    __tablename__ = 'sys_login_log'

    id: Mapped[id_key] = mapped_column(init=False)
    user_uuid: Mapped[str] = mapped_column(String(50), comment='userUUID')
    username: Mapped[str] = mapped_column(String(20), comment='userName')
    status: Mapped[int] = mapped_column(insert_default=0, comment='Login status(0Failure 1Success)')
    ip: Mapped[str] = mapped_column(String(50), comment='loginIPAddress')
    country: Mapped[str | None] = mapped_column(String(50), comment='Country')
    region: Mapped[str | None] = mapped_column(String(50), comment='Area')
    city: Mapped[str | None] = mapped_column(String(50), comment='City')
    user_agent: Mapped[str] = mapped_column(String(255), comment='Request header')
    os: Mapped[str | None] = mapped_column(String(50), comment='Operating System')
    browser: Mapped[str | None] = mapped_column(String(50), comment='Browser')
    device: Mapped[str | None] = mapped_column(String(50), comment='Equipment')
    msg: Mapped[str] = mapped_column(LONGTEXT, comment='Prompt message')
    login_time: Mapped[datetime] = mapped_column(comment='logintime')
    created_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='Creation time')
