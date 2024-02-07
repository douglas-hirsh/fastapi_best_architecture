#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field

from backend.app.common.enums import MethodType
from backend.app.schemas.base import SchemaBase


class CreatePolicyParam(SchemaBase):
    sub: str = Field(..., description='useruuid / RoleID')
    path: str = Field(..., description='api Path')
    method: MethodType = Field(default=MethodType.GET, description='Request method')


class UpdatePolicyParam(CreatePolicyParam):
    pass


class DeletePolicyParam(CreatePolicyParam):
    pass


class DeleteAllPoliciesParam(SchemaBase):
    uuid: str | None = None
    role: str


class CreateUserRoleParam(SchemaBase):
    uuid: str = Field(..., description='user uuid')
    role: str = Field(..., description='Role')


class DeleteUserRoleParam(CreateUserRoleParam):
    pass


class GetPolicyListDetails(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ptype: str = Field(..., description='Rule type., p / g')
    v0: str = Field(..., description='user uuid / Role')
    v1: str = Field(..., description='api Path / Role')
    v2: str | None = None
    v3: str | None = None
    v4: str | None = None
    v5: str | None = None
