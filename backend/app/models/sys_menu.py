#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key
from backend.app.models.sys_role_menu import sys_role_menu


class Menu(Base):
    """Menu"""

    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(50), comment='Menu Title')
    name: Mapped[str] = mapped_column(String(50), comment='Menu Name')
    level: Mapped[int] = mapped_column(default=0, comment='Menu hierarchy')
    sort: Mapped[int] = mapped_column(default=0, comment='Sorting')
    icon: Mapped[str | None] = mapped_column(String(100), default=None, comment='Menu icon')
    path: Mapped[str | None] = mapped_column(String(200), default=None, comment='Routing address')
    menu_type: Mapped[int] = mapped_column(default=0, comment='Menu type(0Table of contents 1Menu 2button) ')
    component: Mapped[str | None] = mapped_column(String(255), default=None, comment='component path')
    perms: Mapped[str | None] = mapped_column(String(100), default=None, comment='Authorization identifier')
    status: Mapped[int] = mapped_column(default=1, comment='Menustatus(0discontinue 1Normal) ')
    show: Mapped[int] = mapped_column(default=1, comment='Display(0No. 1is) ')
    cache: Mapped[int] = mapped_column(default=1, comment='isNo.Cache(0No. 1is) ')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='Remark')
    # fatherMenuone-to-many
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_menu.id', ondelete='SET NULL'), default=None, index=True, comment='FatherMenuID'
    )
    parent: Mapped[Union['Menu', None]] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list['Menu'] | None] = relationship(init=False, back_populates='parent')
    # MenuMany-to-many
    roles: Mapped[list['Role']] = relationship(  # noqa: F821
        init=False, secondary=sys_role_menu, back_populates='menus'
    )
