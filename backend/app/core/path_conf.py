#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from pathlib import Path

# Get project root directory
# Or use absolute path,point atbackendTo the directory.,For examplewindows: BasePath = D:\git_project\fastapi_mysql\backend
BasePath = Path(__file__).resolve().parent.parent.parent

# Migration file storage path.
Versions = os.path.join(BasePath, 'app', 'alembic', 'versions')

# Log file path
LogPath = os.path.join(BasePath, 'app', 'log')

# Offline IP Database path
IP2REGION_XDB = os.path.join(BasePath, 'app', 'static', 'ip2region.xdb')
