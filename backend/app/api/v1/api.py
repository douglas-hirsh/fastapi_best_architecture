#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.api import CreateApiParam, GetApiListDetails, UpdateApiParam
from backend.app.services.api_service import api_service

router = APIRouter()


@router.get('/all', summary='Get all interfaces', dependencies=[DependsJwtAuth])
async def get_all_apis() -> ResponseModel:
    data = await api_service.get_api_list()
    return await response_base.success(data=data)


@router.get('/{pk}', summary='Get interface details.', dependencies=[DependsJwtAuth])
async def get_api(pk: Annotated[int, Path(...)]) -> ResponseModel:
    api = await api_service.get(pk=pk)
    return await response_base.success(data=api)


@router.get(
    '',
    summary='(Fuzzy condition) paginationGet all interfaces',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_apis(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    method: Annotated[str | None, Query()] = None,
    path: Annotated[str | None, Query()] = None,
) -> ResponseModel:
    api_select = await api_service.get_select(name=name, method=method, path=path)
    page_data = await paging_data(db, api_select, GetApiListDetails)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='create',
    dependencies=[
        Depends(RequestPermission('sys:api:add')),
        DependsRBAC,
    ],
)
async def create_api(obj: CreateApiParam) -> ResponseModel:
    await api_service.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='Update interface',
    dependencies=[
        Depends(RequestPermission('sys:api:edit')),
        DependsRBAC,
    ],
)
async def update_api(pk: Annotated[int, Path(...)], obj: UpdateApiParam) -> ResponseModel:
    count = await api_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='(batch) Delete interface',
    dependencies=[
        Depends(RequestPermission('sys:api:del')),
        DependsRBAC,
    ],
)
async def delete_api(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await api_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
