# circuit -*- python -*-
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2020 Jeff Epler

import time

YEAR_BASE = 1900
EPOCH_YEAR = 1970
EPOCH_WDAY = 4
EPOCH_YEARS_SINCE_LEAP = 2
EPOCH_YEARS_SINCE_CENTURY = 70
EPOCH_YEARS_SINCE_LEAP_CENTURY = 370
SECSPERDAY = 86400
SECSPERHOUR = 3600
DAYSPERWEEK = 7

month_lengths = [
    b"\x1f\x1c\x1f\x1e\x1f\x1e\x1f\x1f\x1e\x1f\x1e\x1f",
    b"\x1f\x1d\x1f\x1e\x1f\x1e\x1f\x1f\x1e\x1f\x1e\x1f",
]

if hasattr(time, "gmtime"):
    gmtime = time.gmtime
else:
    gmtime = time.localtime


def isleap(year):
    return (((year) % 4) == 0 and ((year) % 100) != 0) or ((year) % 400) == 0


class TzInfo:
    @classmethod
    def localtime(cls, utc=None):
        if utc is None:
            utc = time.time()
        is_dst = cls.dstrule(utc)
        offset = cls.altzone if is_dst else cls.timezone
        r = gmtime(utc - offset)
        return time.struct_time(r[:8] + (is_dst,))


class MRuleTimeZone(TzInfo):
    @classmethod
    def dstrule(cls, utc):
        r = gmtime(utc - cls.timezone)
        cls._calc(r.tm_year)
        if cls._north:
            return utc >= cls._change[0] and utc < cls._change[1]
        else:
            return utc >= cls._change[0] or utc < cls._change[1]

    @classmethod
    def _calc(cls, year):
        if cls._year == year:
            return
        cls._year = year
        cls._change = (
            cls._calc1(year, cls.timezone, *cls.start),
            cls._calc1(year, cls.altzone, *cls.end),
        )
        cls._north = cls._change[0] < cls._change[1]

    @classmethod
    def _calc1(cls, year, offset, m, n, d):
        year = year - EPOCH_YEAR
        yleap = isleap(year)
        days = (
            year * 365
            + (year - 1 + EPOCH_YEARS_SINCE_LEAP) // 4
            - (year - 1 + EPOCH_YEARS_SINCE_CENTURY) // 100
            + (year - 1 + EPOCH_YEARS_SINCE_LEAP_CENTURY) // 400
        )

        lengths = month_lengths[yleap]

        for j in range(1, m):
            days += lengths[j - 1]

        m_wday = (EPOCH_WDAY + days) % DAYSPERWEEK
        wday_diff = d - m_wday
        if wday_diff < 0:
            wday_diff += DAYSPERWEEK
        m_day = (n - 1) * DAYSPERWEEK + wday_diff

        while m_day >= lengths[j - 1]:
            m_day -= DAYSPERWEEK

        days += m_day

        return offset + days * SECSPERDAY + 2 * SECSPERHOUR

    _year = None
    _north = None
    _change = None
