#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.mysql import JSON, LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import DataClassBase, id_key
from backend.app.utils.timezone import timezone


class OperaLog(DataClassBase):
    """Operation log table"""

    __tablename__ = 'sys_opera_log'

    id: Mapped[id_key] = mapped_column(init=False)
    username: Mapped[str | None] = mapped_column(String(20), comment='Username')
    method: Mapped[str] = mapped_column(String(20), comment='request type')
    title: Mapped[str] = mapped_column(String(255), comment='Operation module')
    path: Mapped[str] = mapped_column(String(500), comment='Request path')
    ip: Mapped[str] = mapped_column(String(50), comment='IPAddress')
    country: Mapped[str | None] = mapped_column(String(50), comment='Country')
    region: Mapped[str | None] = mapped_column(String(50), comment='Area')
    city: Mapped[str | None] = mapped_column(String(50), comment='City')
    user_agent: Mapped[str] = mapped_column(String(255), comment='Request header')
    os: Mapped[str | None] = mapped_column(String(50), comment='Operating System')
    browser: Mapped[str | None] = mapped_column(String(50), comment='Browser')
    device: Mapped[str | None] = mapped_column(String(50), comment='Equipment')
    args: Mapped[str | None] = mapped_column(JSON(), comment='Request parameters')
    status: Mapped[int] = mapped_column(comment='Operation status(0abnormal 1Normal) ')
    code: Mapped[str] = mapped_column(String(20), insert_default='200', comment='Operation statuscode')
    msg: Mapped[str | None] = mapped_column(LONGTEXT, comment='Prompt message')
    cost_time: Mapped[float] = mapped_column(insert_default=0.0, comment='Request Durationms')
    opera_time: Mapped[datetime] = mapped_column(comment='operation time')
    created_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='Creation time')
