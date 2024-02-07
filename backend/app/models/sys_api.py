#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base, id_key


class Api(Base):
    """systemapi"""

    __tablename__ = 'sys_api'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='apiName')
    method: Mapped[str] = mapped_column(String(16), comment='Request method')
    path: Mapped[str] = mapped_column(String(500), comment='apiPath')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, comment='Remark')
