#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from backend.app.models.base import MappedBase

sys_user_role = Table(
    'sys_user_role',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='primary keyID'),
    Column('user_id', Integer, ForeignKey('sys_user.id', ondelete='CASCADE'), primary_key=True, comment='userID'),
    Column('role_id', Integer, ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='RoleID'),
)
