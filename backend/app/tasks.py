#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import uuid

sys.path.append('../../')

from backend.app.common.celery import celery_app  # noqa: E402


@celery_app.task
def task_demo_async() -> str:
    uid = uuid.uuid4().hex
    print(f'Asynchronous task {uid} Execution successful')
    return uid
