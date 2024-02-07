#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Import all models,and Base Put it in front., So that Base Have them.
# imported by Alembic
"""
from backend.app.models.base import MappedBase
from backend.app.models.sys_api import Api
from backend.app.models.sys_casbin_rule import CasbinRule
from backend.app.models.sys_dept import Dept
from backend.app.models.sys_dict_data import DictData
from backend.app.models.sys_dict_type import DictType
from backend.app.models.sys_login_log import LoginLog
from backend.app.models.sys_menu import Menu
from backend.app.models.sys_opera_log import OperaLog
from backend.app.models.sys_role import Role
from backend.app.models.sys_user import User
