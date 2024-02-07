#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request

from backend.app.common.exception import errors
from backend.app.core.conf import settings


async def demo_site(request: Request):
    """Demo site"""

    method = request.method
    path = request.url.path
    if (
        settings.DEMO_MODE
        and method != 'GET'
        and method != 'OPTIONS'
        and (method, path) not in settings.DEMO_MODE_EXCLUDE
    ):
        raise errors.ForbiddenError(msg='Prohibited from executing this action in the demonstration environment.')
