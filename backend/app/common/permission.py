#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request

from backend.app.common.exception.errors import ServerError
from backend.app.core.conf import settings


class RequestPermission:
    """
    Request permission,Only used for character menu.RBAC

    Tip:
        Use thisRequest permissiontime,need `Depends(RequestPermission('xxx'))` In `DependsRBAC` before,
        because fastapi The current version of the interface dependency injection is executed in ascending order. 
        RBAC IdentificationInVerification before setting
    """

    def __init__(self, value: str):
        self.value = value

    async def __call__(self, request: Request):
        if settings.PERMISSION_MODE == 'role-menu':
            if not isinstance(self.value, str):
                raise ServerError
            # Additional permission identifier
            request.state.permission = self.value
