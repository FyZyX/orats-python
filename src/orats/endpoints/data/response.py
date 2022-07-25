import datetime
from typing import Generic, Optional, Sequence, TypeVar

from pydantic import validator
from pydantic.generics import GenericModel

from orats.constructs.api.data import DataApiConstruct
from orats.errors import OratsError


def parse_date(dt: datetime.date):
    return dt.strftime("%Y/%m/%d")


T = TypeVar("T", bound=DataApiConstruct)


class DataApiResponse(GenericModel, Generic[T]):
    data: Optional[Sequence[T]]
    message: Optional[str]
    error: Optional[str]

    @validator("error", "message")
    def check_failures(cls, v):
        if v is not None:
            raise OratsError(v)
        return v
