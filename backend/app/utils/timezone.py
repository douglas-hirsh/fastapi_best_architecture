#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zoneinfo

from datetime import datetime

from backend.app.core.conf import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE):
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        """
        Obtain time zone time

        :return:
        """
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        """
        datetime Timezone time

        :param dt:
        :return:
        """
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        Time string to time zone time

        :param date_str:
        :param format_str:
        :return:
        """
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)


timezone = TimeZone()
