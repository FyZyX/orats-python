import os
from typing import TYPE_CHECKING, Optional, Generic, TypeVar

from pydantic import Field, PrivateAttr
from pydantic.generics import GenericModel

if TYPE_CHECKING:
    from orats.endpoints import data as endpoints


def _get_token() -> str:
    return os.environ.get("ORATS_API_TOKEN", "demo")


class Construct(GenericModel):
    _level: int
    _token: Optional[str] = Field(_get_token(), description="API token.")


class ApiConstruct(Construct):
    _level = 0


L0 = TypeVar("L0", bound=ApiConstruct)
Req = TypeVar("Req")
Res = TypeVar("Res")


class IndustryConstruct(Construct, Generic[L0]):
    _level = 1
    _cache: Optional[L0] = PrivateAttr(None)

    def _make_request(
        self,
        endpoint: "endpoints.DataApiEndpoint[Req, Res]",
        request: Req,
    ) -> Res:
        if self._cache:
            return self._cache

        self._cache = endpoint(request)[0]
        return self._cache


L1 = TypeVar("L1", bound=IndustryConstruct)


class ApplicationConstruct(Construct):
    _level = 2
