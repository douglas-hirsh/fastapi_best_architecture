#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, Field

from backend.app.common.enums import StatusType


class DictTypeBase(BaseModel):
    name: str
    code: str
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateDictType(DictTypeBase):
    pass


class UpdateDictType(DictTypeBase):
    pass


class GetAllDictType(DictTypeBase):
    id: int
    create_user: int
    update_user: int = None
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True