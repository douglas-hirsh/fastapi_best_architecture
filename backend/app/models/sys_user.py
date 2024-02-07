#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.db_mysql import uuid4_str
from backend.app.models.base import Base, id_key
from backend.app.models.sys_user_role import sys_user_role
from backend.app.utils.timezone import timezone


class User(Base):
    """User table"""

    __tablename__ = 'sys_user'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String(50), init=False, default_factory=uuid4_str, unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='Username')
    nickname: Mapped[str] = mapped_column(String(20), unique=True, comment='nickname')
    password: Mapped[str] = mapped_column(String(255), comment='Password')
    salt: Mapped[str] = mapped_column(String(5), comment='Salt')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment='Email')
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='Super privilege(0No. 1is)')
    is_staff: Mapped[bool] = mapped_column(default=False, comment='Login for backstage management(0No. 1is)')
    status: Mapped[int] = mapped_column(default=1, comment='User account status(0discontinue 1Normal)')
    is_multi_login: Mapped[bool] = mapped_column(default=False, comment='isNo.Repeated login.(0No. 1is)')
    avatar: Mapped[str | None] = mapped_column(String(255), default=None, comment='Profile picture')
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='Mobile number')
    join_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='Registration time')
    last_login_time: Mapped[datetime | None] = mapped_column(init=False, onupdate=timezone.now, comment='Last login.')
    # Department users one-to-many.
    dept_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None, comment='Department correlationID'
    )
    dept: Mapped[Union['Dept', None]] = relationship(init=False, back_populates='users')  # noqa: F821
    # User role multiple to multiple.
    roles: Mapped[list['Role']] = relationship(  # noqa: F821
        init=False, secondary=sys_user_role, back_populates='users'
    )
