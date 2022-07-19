import os
from typing import TYPE_CHECKING, Optional, Generic, TypeVar

from pydantic import Field, PrivateAttr
from pydantic.generics import GenericModel

if TYPE_CHECKING:
    from orats.endpoints import data as endpoints
    from orats.constructs.api.data import request as req
    from orats.constructs.api.data import response as res


def _get_token() -> str:
    return os.environ.get("ORATS_API_TOKEN", "demo")


class Construct(GenericModel):
    _level: int
    _token: str = Field(_get_token(), description="API token.")


class ApiConstruct(Construct):
    _level = 0


Req = TypeVar("Req", bound="req.DataApiRequest")
Res = TypeVar("Res", bound="res.DataApiConstruct")


class IndustryConstruct(Construct, Generic[Req, Res]):
    _level = 1
    _cache: Optional[Res] = PrivateAttr(None)

    def _make_request(
        self,
        endpoint: "endpoints.DataApiEndpoint[Req, Res]",
        request: Req,
    ) -> Res:
        if self._cache:
            return self._cache

        self._cache = endpoint(request)[0]
        return self._cache


class ApplicationConstruct(Construct):
    _level = 2
