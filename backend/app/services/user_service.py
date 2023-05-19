#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email_validator import validate_email, EmailNotValidError
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.common import jwt
from backend.app.common.exception import errors
from backend.app.crud.crud_dept import DeptDao
from backend.app.crud.crud_role import RoleDao
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.user import CreateUser, ResetPassword, UpdateUser, Avatar, Auth
from backend.app.utils import re_verify


class UserService:
    @staticmethod
    async def swagger_login(form_data: OAuth2PasswordRequestForm):
        async with async_db_session() as db:
            current_user = await UserDao.get_user_by_username(db, form_data.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户名不存在')
            elif not jwt.password_verify(form_data.password, current_user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not current_user.is_active:
                raise errors.AuthorizationError(msg='该用户已被锁定，无法登录')
            # 更新登陆时间
            await UserDao.update_user_login_time(db, form_data.username)
            # 查询用户角色
            user_role_ids = await UserDao.get_user_role_ids(db, current_user.id)
            # 获取最新用户信息
            user = await UserDao.get_user_by_id(db, current_user.id)
            # 创建token
            access_token = await jwt.create_access_token(user.id, role_ids=user_role_ids)
            return access_token, user

    @staticmethod
    async def login(obj: Auth):
        async with async_db_session() as db:
            current_user = await UserDao.get_user_by_username(db, obj.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户名不存在')
            elif not jwt.password_verify(obj.password, current_user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not current_user.is_active:
                raise errors.AuthorizationError(msg='该用户已被锁定，无法登录')
            await UserDao.update_user_login_time(db, obj.username)
            user_role_ids = await UserDao.get_user_role_ids(db, current_user.id)
            user = await UserDao.get_user_by_id(db, current_user.id)
            access_token = await jwt.create_access_token(user.id, role_ids=user_role_ids)
            return access_token, user

    @staticmethod
    async def register(obj: CreateUser):
        async with async_db_session.begin() as db:
            username = await UserDao.get_user_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='该用户名已注册')
            email = await UserDao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
            try:
                validate_email(obj.email, check_deliverability=False).email
            except EmailNotValidError:
                raise errors.ForbiddenError(msg='邮箱格式错误')
            dept = await DeptDao.get_dept_by_id(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await RoleDao.get_role_by_id(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            await UserDao.create_user(db, obj)

    @staticmethod
    async def pwd_reset(obj: ResetPassword):
        async with async_db_session.begin() as db:
            pwd1 = obj.password1
            pwd2 = obj.password2
            if pwd1 != pwd2:
                raise errors.ForbiddenError(msg='两次密码输入不一致')
            await UserDao.reset_password(db, obj.id, obj.password2)

    @staticmethod
    async def get_userinfo(username: str):
        async with async_db_session() as db:
            user = await UserDao.get_user_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user

    @staticmethod
    async def update(*, username: str, current_user: User, obj: UpdateUser):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_user_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            if input_user.username != obj.username:
                username = await UserDao.get_user_by_username(db, obj.username)
                if username:
                    raise errors.ForbiddenError(msg='该用户名已存在')
            if input_user.email != obj.email:
                _email = await UserDao.check_email(db, obj.email)
                if _email:
                    raise errors.ForbiddenError(msg='该邮箱已注册')
                try:
                    validate_email(obj.email, check_deliverability=False).email
                except EmailNotValidError:
                    raise errors.ForbiddenError(msg='邮箱格式错误')
            if obj.phone is not None:
                if not re_verify.is_phone(obj.phone):
                    raise errors.ForbiddenError(msg='手机号码输入有误')
            dept = await DeptDao.get_dept_by_id(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await RoleDao.get_role_by_id(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            count = await UserDao.update_userinfo(db, input_user, obj)
            return count

    @staticmethod
    async def update_avatar(*, username: str, current_user: User, avatar: Avatar):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_user_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await UserDao.update_avatar(db, input_user, avatar)
            return count

    @staticmethod
    async def get_user_list():
        return UserDao.get_users()

    @staticmethod
    async def update_permission(pk: int):
        async with async_db_session.begin() as db:
            if await UserDao.get_user_by_id(db, pk):
                count = await UserDao.super_set(db, pk)
                return count
            else:
                raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def update_active(pk: int):
        async with async_db_session.begin() as db:
            if await UserDao.get_user_by_id(db, pk):
                count = await UserDao.active_set(db, pk)
                return count
            else:
                raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def delete(*, username: str, current_user: User):
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_user_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await UserDao.delete_user(db, input_user.id)
            return count