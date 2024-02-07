#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key


class DictData(Base):
    """dictionary"""

    __tablename__ = 'sys_dict_data'

    id: Mapped[id_key] = mapped_column(init=False)
    label: Mapped[str] = mapped_column(String(32), unique=True, comment='Dictionary Tags')
    value: Mapped[str] = mapped_column(String(32), unique=True, comment='Dictionary value.')
    sort: Mapped[int] = mapped_column(default=0, comment='Sorting')
    status: Mapped[int] = mapped_column(default=1, comment='status(0discontinue 1Normal) ')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='Remark')
    # Dictionary type one to many
    type_id: Mapped[int] = mapped_column(ForeignKey('sys_dict_type.id'), default=None, comment='Dictionary type associationID')
    type: Mapped['DictType'] = relationship(init=False, back_populates='datas')  # noqa: F821
