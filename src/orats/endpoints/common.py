import datetime
import random
import string
from typing import Collection, TypeAlias, Dict, Any

Json: TypeAlias = Dict[str, Any]


def round_value(value, precision=None):
    if precision:
        return round(value, precision)
    return value


def format_timestamp(ts) -> str:
    if isinstance(ts, datetime.datetime):
        return f"{ts.isoformat()}Z"
    elif isinstance(ts, datetime.date):
        return str(ts)
    else:
        raise ValueError


def as_response(construct_type, value):
    return construct_type(**value)


def as_responses(construct_type, values):
    return [as_response(construct_type, value) for value in values]


def random_symbol() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=random.randint(1, 4)))


def universe() -> Collection[str]:
    return {random_symbol() for _ in range(5000)}


def offset_date(date, offset) -> str:
    return format_timestamp(date + datetime.timedelta(days=offset))


def offset_value(value, offset):
    if isinstance(value, int):
        return value + random.randint(0, 2 * offset) - offset
    elif isinstance(value, float):
        return value + random_pos_neg_value(offset)
    else:
        raise ValueError


def random_increase(value, scalar=1, precision=None):
    return round_value(value + scalar * random.random(), precision=precision)


def random_decrease(value, scalar: float = 1, precision=None):
    return round_value(value - scalar * random.random(), precision=precision)


def random_pos_neg_value(scalar=1):
    return 2 * scalar * (random.random() - 0.5)


def positive_integer(max_value=200):
    return random.randint(0, max_value)


def random_value(scalar: float = 1, precision=None):
    return round_value(scalar * random.random(), precision=precision)


def quote(value, bid=False, ask=False):
    if not (bid or ask):
        raise ValueError
    sign = 1
    if bid:
        sign = -1
    return round(value + sign * random.random(), 2)
