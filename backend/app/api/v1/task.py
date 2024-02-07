#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_code import CustomResponseCode
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.services.task_service import task_service

router = APIRouter()


@router.get('', summary='get all executable task modules', dependencies=[DependsJwtAuth])
async def get_all_tasks() -> ResponseModel:
    tasks = task_service.get_task_list()
    return await response_base.success(data=tasks)


@router.get('/{pk}', summary='Get task results', dependencies=[DependsJwtAuth])
async def get_task_result(pk: Annotated[str, Path(description='taskID')]) -> ResponseModel:
    task = task_service.get(pk)
    if not task:
        return await response_base.fail(res=CustomResponseCode.HTTP_204, data=pk)
    return await response_base.success(data=task.result)


@router.post(
    '/{module}',
    summary='executetask',
    dependencies=[
        Depends(RequestPermission('sys:task:run')),
        DependsRBAC,
    ],
)
async def run_task(
    module: Annotated[str, Path(description='taskModule')],
    args: Annotated[list | None, Body()] = None,
    kwargs: Annotated[dict | None, Body()] = None,
) -> ResponseModel:
    task = task_service.run(module=module, args=args, kwargs=kwargs)
    return await response_base.success(data=task.result)
