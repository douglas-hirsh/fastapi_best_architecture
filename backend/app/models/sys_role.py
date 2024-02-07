#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key
from backend.app.models.sys_role_menu import sys_role_menu
from backend.app.models.sys_user_role import sys_user_role


class Role(Base):
    """Role table"""

    __tablename__ = 'sys_role'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='Role Name')
    data_scope: Mapped[int | None] = mapped_column(default=2, comment='Scope of authority(1: All data permissions 2: Custom data permissions) ')
    status: Mapped[int] = mapped_column(default=1, comment='Role status(0discontinue 1Normal) ')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='Remark')
    # Multi-to-many role-user
    users: Mapped[list['User']] = relationship(  # noqa: F821
        init=False, secondary=sys_user_role, back_populates='roles'
    )
    # Multiple roles menu
    menus: Mapped[list['Menu']] = relationship(  # noqa: F821
        init=False, secondary=sys_role_menu, back_populates='roles'
    )
