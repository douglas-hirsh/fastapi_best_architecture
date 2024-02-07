#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from backend.app.models.base import MappedBase

sys_role_menu = Table(
    'sys_role_menu',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='primary keyID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='RoleID'),
    Column('menu_id', Integer, ForeignKey('sys_menu.id', ondelete='CASCADE'), primary_key=True, comment='MenuID'),
)
