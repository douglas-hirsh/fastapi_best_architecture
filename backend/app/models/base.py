#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from backend.app.utils.timezone import timezone

# Universal Mapped Primary key., Need manual addition.,Reference the following usage methods.
# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='primary keyid')
]


# Mixin: Object-oriented programming concept, Make the structure clearer., `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
class UserMixin(MappedAsDataclass):
    """user Mixin Data"""

    create_user: Mapped[int] = mapped_column(sort_order=998, comment='creator')
    update_user: Mapped[int | None] = mapped_column(init=False, default=None, sort_order=998, comment='Modifier')


class DateTimeMixin(MappedAsDataclass):
    """Date and time Mixin Data"""

    created_time: Mapped[datetime] = mapped_column(
        init=False, default_factory=timezone.now, sort_order=999, comment='Creation time'
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        init=False, onupdate=timezone.now, sort_order=999, comment='Update time'
    )


class MappedBase(DeclarativeBase):
    """
    declarative base class, original DeclarativeBase type, As all basestypeortypeFather'stypeexist

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    declarativeDatabasetype, it will haveDataintegrated, permit, But you must pay attention to some of its characteristics., especially DeclarativeBase Together when using.

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """  # noqa: E501

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    """
    declarative Mixin Databasetype, WithDataintegrated, And include. MiXin Database, Basic table structure
    """  # noqa: E501

    __abstract__ = True
