from datetime import datetime
from pathlib import Path
from typing import Union

import consts
from . import radioboss


def get_broadcast_num(dt: datetime = None) -> Union[bool, int]:
    if not dt:
        dt = datetime.now()

    day = dt.weekday()
    time = dt.hour * 60 + dt.minute

    for num, (time_start, time_stop) in consts.broadcast_times_[day].items():
        if time_start < time < time_stop:
            return num

    return False


def get_broadcast_name(time: int) -> str:
    return consts.times_name['times'][time]


def is_broadcast_now(day: int, time: int) -> bool:
    return day == datetime.today().weekday() and time is get_broadcast_num()


async def get_broadcast_freetime(day, time):
    break_start, break_finish = consts.broadcast_times_[day][time]
    if is_broadcast_now(day, time):
        last_order = await radioboss.get_new_order_pos()
        if not last_order:
            return 0
        start = last_order['time_start'].hour * 60 + last_order['time_start'].minute
    else:
        try:
            tracks_count = len(list(get_broadcast_path(day, time).iterdir()))
        except FileNotFoundError:
            tracks_count = 0
        start = break_start + tracks_count * 3  # 3 минуты - средняя длина трека

    return max(0, break_finish - start)


def get_broadcast_path(day: int, time: int = False) -> Path:
    t = consts.paths['orders']
    t /= '{0} {1}'.format(day + 1, consts.times_name['week_days'][day])
    if time is not False:  # сука 0 считается как False
        t /= '{0} {1}'.format(time, consts.times_name['times'][time])
    return t
