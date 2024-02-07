#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key


class DictType(Base):
    """Dictionary"""

    __tablename__ = 'sys_dict_type'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(32), unique=True, comment='DictionaryName')
    code: Mapped[str] = mapped_column(String(32), unique=True, comment='DictionaryEncoding')
    status: Mapped[int] = mapped_column(default=1, comment='status(0discontinue 1Normal) ')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='Remark')
    # Dictionaryone-to-many
    datas: Mapped[list['DictData']] = relationship(init=False, back_populates='type')  # noqa: F821
