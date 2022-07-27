from pydantic import Field
from pydantic.generics import GenericModel

from orats.common import get_token


class Construct(GenericModel):
    _level: int
    _token: str = Field(get_token(), description="API token.")


class ApiConstruct(Construct):
    _level = 0


class IndustryConstruct(Construct):
    _level = 1


class ApplicationConstruct(Construct):
    _level = 2
