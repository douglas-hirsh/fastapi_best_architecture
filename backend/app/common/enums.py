#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Type


class _EnumBase:
    @classmethod
    def get_member_keys(cls: Type[Enum]) -> list[str]:
        return [name for name in cls.__members__.keys()]

    @classmethod
    def get_member_values(cls: Type[Enum]) -> list:
        return [item.value for item in cls.__members__.values()]


class IntEnum(_EnumBase, SourceIntEnum):
    """integer enumeration"""

    pass


class StrEnum(_EnumBase, str, Enum):
    """String enumeration"""

    pass


class MenuType(IntEnum):
    """Menu type"""

    directory = 0
    menu = 1
    button = 2


class RoleDataScopeType(IntEnum):
    """data range"""

    all = 1
    custom = 2


class MethodType(StrEnum):
    """Request method"""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'


class LoginLogStatusType(IntEnum):
    """Login log status"""

    fail = 0
    success = 1


class BuildTreeType(StrEnum):
    """Build tree-like structure type"""

    traversal = 'traversal'
    recursive = 'recursive'


class OperaLogCipherType(IntEnum):
    """Operation log encryption type"""

    aes = 0
    md5 = 1
    itsdangerous = 2
    plan = 3


class StatusType(IntEnum):
    """Status type"""

    disable = 0
    enable = 1
