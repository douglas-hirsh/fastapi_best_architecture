#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from fastapi import Request
from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.common.jwt import get_token, password_verify, superuser_verify
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_dept import dept_dao
from backend.app.crud.crud_role import role_dao
from backend.app.crud.crud_user import user_dao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.user import (
    AddUserParam,
    AvatarParam,
    RegisterUserParam,
    ResetPasswordParam,
    UpdateUserParam,
    UpdateUserRoleParam,
)


class UserService:
    @staticmethod
    async def register(*, obj: RegisterUserParam) -> None:
        async with async_db_session.begin() as db:
            username = await user_dao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='The username has already been registered.')
            obj.nickname = obj.nickname if obj.nickname else f'user{random.randrange(10000, 99999)}'
            nickname = await user_dao.get_by_nickname(db, obj.nickname)
            if nickname:
                raise errors.ForbiddenError(msg='Nickname registered')
            email = await user_dao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='The email has been registered.')
            await user_dao.create(db, obj)

    @staticmethod
    async def add(*, request: Request, obj: AddUserParam) -> None:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            username = await user_dao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='ThisuserName already registered')
            obj.nickname = obj.nickname if obj.nickname else f'user{random.randrange(10000, 99999)}'
            nickname = await user_dao.get_by_nickname(db, obj.nickname)
            if nickname:
                raise errors.ForbiddenError(msg='Nickname registered')
            dept = await dept_dao.get(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='Department does not exist')
            for role_id in obj.roles:
                role = await role_dao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='Role does not exist.')
            email = await user_dao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='The email has been registered.')
            await user_dao.add(db, obj)

    @staticmethod
    async def pwd_reset(*, request: Request, obj: ResetPasswordParam) -> int:
        async with async_db_session.begin() as db:
            op = obj.old_password
            if not await password_verify(op + request.user.salt, request.user.password):
                raise errors.ForbiddenError(msg='Incorrect old password.')
            np1 = obj.new_password
            np2 = obj.confirm_password
            if np1 != np2:
                raise errors.ForbiddenError(msg='Passwords entered twice do not match.')
            count = await user_dao.reset_password(db, request.user.id, obj.new_password, request.user.salt)
            prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{request.user.id}:',
            ]
            for i in prefix:
                await redis_client.delete_prefix(i)
            return count

    @staticmethod
    async def get_userinfo(*, username: str) -> User:
        async with async_db_session() as db:
            user = await user_dao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='userdo not exist')
            return user

    @staticmethod
    async def update(*, request: Request, username: str, obj: UpdateUserParam) -> int:
        async with async_db_session.begin() as db:
            if not request.user.is_superuser:
                if request.user.username != username:
                    raise errors.ForbiddenError(msg='You can only modify your own information.')
            input_user = await user_dao.get_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='userdo not exist')
            if input_user.username != obj.username:
                _username = await user_dao.get_by_username(db, obj.username)
                if _username:
                    raise errors.ForbiddenError(msg='TheuserName already exists')
            if input_user.nickname != obj.nickname:
                nickname = await user_dao.get_by_nickname(db, obj.nickname)
                if nickname:
                    raise errors.ForbiddenError(msg='Nickname already exists')
            if input_user.email != obj.email:
                email = await user_dao.check_email(db, obj.email)
                if email:
                    raise errors.ForbiddenError(msg='The email has been registered.')
            count = await user_dao.update_userinfo(db, input_user, obj)
            return count

    @staticmethod
    async def update_roles(*, request: Request, username: str, obj: UpdateUserRoleParam) -> None:
        async with async_db_session.begin() as db:
            if not request.user.is_superuser:
                if request.user.username != username:
                    raise errors.ForbiddenError(msg='You can only modify your own role.')
            input_user = await user_dao.get_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='userdo not exist')
            for role_id in obj.roles:
                role = await role_dao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='Role does not exist.')
            await user_dao.update_role(db, input_user, obj)
            await redis_client.delete_prefix(f'{settings.PERMISSION_REDIS_PREFIX}:{request.user.uuid}')

    @staticmethod
    async def update_avatar(*, request: Request, username: str, avatar: AvatarParam) -> int:
        async with async_db_session.begin() as db:
            if not request.user.is_superuser:
                if request.user.username != username:
                    raise errors.ForbiddenError(msg='You can only edit your own profile picture.')
            input_user = await user_dao.get_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='userdo not exist')
            count = await user_dao.update_avatar(db, input_user, avatar)
            return count

    @staticmethod
    async def get_select(*, dept: int, username: str = None, phone: str = None, status: int = None) -> Select:
        return await user_dao.get_all(dept=dept, username=username, phone=phone, status=status)

    @staticmethod
    async def update_permission(*, request: Request, pk: int) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            if not await user_dao.get(db, pk):
                raise errors.NotFoundError(msg='userdo not exist')
            else:
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='Prohibit modifying own administrator privileges.')
                count = await user_dao.set_super(db, pk)
                return count

    @staticmethod
    async def update_staff(*, request: Request, pk: int) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            if not await user_dao.get(db, pk):
                raise errors.NotFoundError(msg='userdo not exist')
            else:
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='Prohibit modifying self-backend management login permissions.')
                count = await user_dao.set_staff(db, pk)
                return count

    @staticmethod
    async def update_status(*, request: Request, pk: int) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            if not await user_dao.get(db, pk):
                raise errors.NotFoundError(msg='userdo not exist')
            else:
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='Prohibited modifying own state')
                count = await user_dao.set_status(db, pk)
                return count

    @staticmethod
    async def update_multi_login(*, request: Request, pk: int) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            if not await user_dao.get(db, pk):
                raise errors.NotFoundError(msg='userdo not exist')
            else:
                count = await user_dao.set_multi_login(db, pk)
                token = await get_token(request)
                user_id = request.user.id
                latest_multi_login = await user_dao.get_multi_login(db, pk)
                # TODO: Removeuser refresh token, This operation requires passing arguments.,Not considering implementation for now.
                # currentusermodify oneself(ordinary/super) ,Except the currenttokenOutside,othertokenFailure
                if pk == user_id:
                    if not latest_multi_login:
                        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{pk}:'
                        await redis_client.delete_prefix(prefix, exclude=prefix + token)
                # superusermodifyOtherstime,Otherstokenwill (all)Failure
                else:
                    if not latest_multi_login:
                        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{pk}:'
                        await redis_client.delete_prefix(prefix)
                return count

    @staticmethod
    async def delete(*, username: str) -> int:
        async with async_db_session.begin() as db:
            input_user = await user_dao.get_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='userdo not exist')
            count = await user_dao.delete(db, input_user.id)
            prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{input_user.id}:',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{input_user.id}:',
            ]
            for i in prefix:
                await redis_client.delete_prefix(i)
            return count


user_service: UserService = UserService()
