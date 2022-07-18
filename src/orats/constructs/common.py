import os
from typing import Optional, Generic, TypeVar

from pydantic import Field, PrivateAttr
from pydantic.generics import GenericModel


def _get_token() -> str:
    return os.environ.get("ORATS_API_TOKEN", "demo")


class Construct(GenericModel):
    _level: int
    _token: Optional[str] = Field(_get_token(), description="API token.")


class ApiConstruct(Construct):
    _level = 0


T = TypeVar("T", bound=ApiConstruct)


class IndustryConstruct(Construct, Generic[T]):
    _level = 1
    _cache: Optional[T] = PrivateAttr(None)

    def _make_request(self, endpoint, request) -> T:
        if self._cache:
            return self._cache

        self._cache = endpoint(request)[0]
        return self._cache


class ApplicationConstruct(Construct):
    _level = 2
