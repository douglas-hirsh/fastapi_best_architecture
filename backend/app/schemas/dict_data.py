#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.common.enums import StatusType
from backend.app.schemas.base import SchemaBase
from backend.app.schemas.dict_type import GetDictTypeListDetails


class DictDataSchemaBase(SchemaBase):
    type_id: int
    label: str
    value: str
    sort: int
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateDictDataParam(DictDataSchemaBase):
    pass


class UpdateDictDataParam(DictDataSchemaBase):
    pass


class GetDictDataListDetails(DictDataSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: GetDictTypeListDetails
    created_time: datetime
    updated_time: datetime | None = None
