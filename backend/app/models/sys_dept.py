#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key


class Dept(Base):
    """Department table"""

    __tablename__ = 'sys_dept'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='Department name')
    level: Mapped[int] = mapped_column(default=0, comment='Department level')
    sort: Mapped[int] = mapped_column(default=0, comment='Sorting')
    leader: Mapped[str | None] = mapped_column(String(20), default=None, comment='Person in charge')
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='mobile phone')
    email: Mapped[str | None] = mapped_column(String(50), default=None, comment='Email')
    status: Mapped[int] = mapped_column(default=1, comment='Department status(0discontinue 1Normal)')
    del_flag: Mapped[bool] = mapped_column(default=False, comment='delete(0Remove 1Existence) ')
    # The translation is: parent department one-to-many
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None, index=True, comment='father departmentID'
    )
    parent: Mapped[Union['Dept', None]] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list['Dept'] | None] = relationship(init=False, back_populates='parent')
    # Department users one-to-many.
    users: Mapped[list['User']] = relationship(init=False, back_populates='dept')  # noqa: F821
