#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.user import (
    AddUserParam,
    AvatarParam,
    GetCurrentUserInfoDetail,
    GetUserInfoListDetails,
    RegisterUserParam,
    ResetPasswordParam,
    UpdateUserParam,
    UpdateUserRoleParam,
)
from backend.app.services.user_service import user_service
from backend.app.utils.serializers import select_as_dict

router = APIRouter()


@router.post('/register', summary='User registration')
async def user_register(obj: RegisterUserParam) -> ResponseModel:
    await user_service.register(obj=obj)
    return await response_base.success()


@router.post('/add', summary='Add user', dependencies=[DependsRBAC])
async def add_user(request: Request, obj: AddUserParam) -> ResponseModel:
    await user_service.add(request=request, obj=obj)
    current_user = await user_service.get_userinfo(username=obj.username)
    data = GetUserInfoListDetails(**await select_as_dict(current_user))
    return await response_base.success(data=data)


@router.post('/password/reset', summary='Reset password', dependencies=[DependsJwtAuth])
async def password_reset(request: Request, obj: ResetPasswordParam) -> ResponseModel:
    count = await user_service.pwd_reset(request=request, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.get('/me', summary='Get current user information.', dependencies=[DependsJwtAuth], response_model_exclude={'password'})
async def get_current_userinfo(request: Request) -> ResponseModel:
    data = GetCurrentUserInfoDetail(**await select_as_dict(request.user))
    return await response_base.success(data=data)


@router.get('/{username}', summary='View user information', dependencies=[DependsJwtAuth])
async def get_user(username: Annotated[str, Path(...)]) -> ResponseModel:
    current_user = await user_service.get_userinfo(username=username)
    data = GetUserInfoListDetails(**await select_as_dict(current_user))
    return await response_base.success(data=data)


@router.put('/{username}', summary='Update user information', dependencies=[DependsJwtAuth])
async def update_userinfo(request: Request, username: Annotated[str, Path(...)], obj: UpdateUserParam) -> ResponseModel:
    count = await user_service.update(request=request, username=username, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.put(
    '/{username}/role',
    summary='Update user roles',
    dependencies=[
        Depends(RequestPermission('sys:user:role:edit')),
        DependsRBAC,
    ],
)
async def update_user_role(
    request: Request, username: Annotated[str, Path(...)], obj: UpdateUserRoleParam
) -> ResponseModel:
    await user_service.update_roles(request=request, username=username, obj=obj)
    return await response_base.success()


@router.put('/{username}/avatar', summary='Update profile picture', dependencies=[DependsJwtAuth])
async def update_avatar(request: Request, username: Annotated[str, Path(...)], avatar: AvatarParam) -> ResponseModel:
    count = await user_service.update_avatar(request=request, username=username, avatar=avatar)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.get(
    '',
    summary='(Fuzzy condition) Pagination to retrieve all users',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_users(
    db: CurrentSession,
    dept: Annotated[int | None, Query()] = None,
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    user_select = await user_service.get_select(dept=dept, username=username, phone=phone, status=status)
    page_data = await paging_data(db, user_select, GetUserInfoListDetails)
    return await response_base.success(data=page_data)


@router.put('/{pk}/super', summary='Modify user super permissions.', dependencies=[DependsRBAC])
async def super_set(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await user_service.update_permission(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.put('/{pk}/staff', summary='Modify user backend login permissions', dependencies=[DependsRBAC])
async def staff_set(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await user_service.update_staff(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.put('/{pk}/status', summary='Modify user status', dependencies=[DependsRBAC])
async def status_set(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await user_service.update_status(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.put('/{pk}/multi', summary='Change user multi-login status.', dependencies=[DependsRBAC])
async def multi_set(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await user_service.update_multi_login(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    path='/{username}',
    summary='User logout',
    description='User logout != User logout,delete',
    dependencies=[
        Depends(RequestPermission('sys:user:del')),
        DependsRBAC,
    ],
)
async def delete_user(username: Annotated[str, Path(...)]) -> ResponseModel:
    count = await user_service.delete(username=username)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
