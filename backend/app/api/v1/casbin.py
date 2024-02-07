#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.casbin_rule import (
    CreatePolicyParam,
    CreateUserRoleParam,
    DeleteAllPoliciesParam,
    DeletePolicyParam,
    DeleteUserRoleParam,
    GetPolicyListDetails,
    UpdatePolicyParam,
)
from backend.app.services.casbin_service import casbin_service

router = APIRouter()


@router.get(
    '',
    summary='(Fuzzy condition) Pagination to get all permission rules',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_casbin(
    db: CurrentSession,
    ptype: Annotated[str | None, Query(description='Rule type., p / g')] = None,
    sub: Annotated[str | None, Query(description='user uuid / Role')] = None,
) -> ResponseModel:
    casbin_select = await casbin_service.get_casbin_list(ptype=ptype, sub=sub)
    page_data = await paging_data(db, casbin_select, GetPolicyListDetails)
    return await response_base.success(data=page_data)


@router.get('/policies', summary='Get allPPermission rules', dependencies=[DependsJwtAuth])
async def get_all_policies(role: Annotated[int | None, Query(description='RoleID')] = None) -> ResponseModel:
    policies = await casbin_service.get_policy_list(role=role)
    return await response_base.success(data=policies)


@router.post(
    '/policy',
    summary='AddPPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:p:add')),
        DependsRBAC,
    ],
)
async def create_policy(p: CreatePolicyParam) -> ResponseModel:
    """
    p Rule:

    - Recommend Add Based on Role Access rights, to cooperate Add g Ruleability,suitable<br>
    **format**: Role role + Access path path + visit method

    - IfAddBased onuserAccess rights, not to cooperateAdd g Ruleable,Suitable configuration specifieduserAccess interface policy<br>
    **format**: user uuid + Access path path + visit method
    """
    data = await casbin_service.create_policy(p=p)
    return await response_base.success(data=data)


@router.post(
    '/policies',
    summary='AddMultiplePPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:add')),
        DependsRBAC,
    ],
)
async def create_policies(ps: list[CreatePolicyParam]) -> ResponseModel:
    data = await casbin_service.create_policies(ps=ps)
    return await response_base.success(data=data)


@router.put(
    '/policy',
    summary='updatePPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:p:edit')),
        DependsRBAC,
    ],
)
async def update_policy(old: UpdatePolicyParam, new: UpdatePolicyParam) -> ResponseModel:
    data = await casbin_service.update_policy(old=old, new=new)
    return await response_base.success(data=data)


@router.put(
    '/policies',
    summary='updateMultiplePPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:edit')),
        DependsRBAC,
    ],
)
async def update_policies(old: list[UpdatePolicyParam], new: list[UpdatePolicyParam]) -> ResponseModel:
    data = await casbin_service.update_policies(old=old, new=new)
    return await response_base.success(data=data)


@router.delete(
    '/policy',
    summary='RemovePPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:p:del')),
        DependsRBAC,
    ],
)
async def delete_policy(p: DeletePolicyParam) -> ResponseModel:
    data = await casbin_service.delete_policy(p=p)
    return await response_base.success(data=data)


@router.delete(
    '/policies',
    summary='RemoveMultiplePPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:del')),
        DependsRBAC,
    ],
)
async def delete_policies(ps: list[DeletePolicyParam]) -> ResponseModel:
    data = await casbin_service.delete_policies(ps=ps)
    return await response_base.success(data=data)


@router.delete(
    '/policies/all',
    summary='RemoveAllPPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:p:empty')),
        DependsRBAC,
    ],
)
async def delete_all_policies(sub: DeleteAllPoliciesParam) -> ResponseModel:
    count = await casbin_service.delete_all_policies(sub=sub)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.get('/groups', summary='Get allGPermission rules', dependencies=[DependsJwtAuth])
async def get_all_groups() -> ResponseModel:
    data = await casbin_service.get_group_list()
    return await response_base.success(data=data)


@router.post(
    '/group',
    summary='AddGPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:g:add')),
        DependsRBAC,
    ],
)
async def create_group(g: CreateUserRoleParam) -> ResponseModel:
    """
    g Rule (**rely p Rule**):

    - If p Rule Middle Add finished Based on Role Access rights, then also need to g RuleMiddleAddBased on user Group Access rights, ability<br>
    **format**: user uuid + Role role

    - If p Strategy Middle Add finished Based on user Access rights, then Add corresponding g Rule Can have direct access rights.<br>
    but what you have is not user Role of All authority, And just a single corresponding. p Rule thus Add Access rights
    """
    data = await casbin_service.create_group(g=g)
    return await response_base.success(data=data)


@router.post(
    '/groups',
    summary='AddMultipleGPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:g:group:add')),
        DependsRBAC,
    ],
)
async def create_groups(gs: list[CreateUserRoleParam]) -> ResponseModel:
    data = await casbin_service.create_groups(gs=gs)
    return await response_base.success(data=data)


@router.delete(
    '/group',
    summary='RemoveGPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:g:del')),
        DependsRBAC,
    ],
)
async def delete_group(g: DeleteUserRoleParam) -> ResponseModel:
    data = await casbin_service.delete_group(g=g)
    return await response_base.success(data=data)


@router.delete(
    '/groups',
    summary='RemoveMultipleGPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:g:group:del')),
        DependsRBAC,
    ],
)
async def delete_groups(gs: list[DeleteUserRoleParam]) -> ResponseModel:
    data = await casbin_service.delete_groups(gs=gs)
    return await response_base.success(data=data)


@router.delete(
    '/groups/all',
    summary='RemoveAllGPermission rules',
    dependencies=[
        Depends(RequestPermission('casbin:g:empty')),
        DependsRBAC,
    ],
)
async def delete_all_groups(uuid: Annotated[UUID, Query(...)]) -> ResponseModel:
    count = await casbin_service.delete_all_groups(uuid=uuid)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
