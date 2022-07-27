from typing import Dict, Sequence, TypeVar

from orats.constructs.api import data as constructs
from orats.endpoints.data import endpoints, request as req


Req = TypeVar("Req", bound=req.DataApiRequest)
Res = TypeVar("Res", bound=constructs.DataApiConstruct)


def cache_request(
    key: str,
    endpoint: endpoints.DataApiEndpoint[Req, Res],
    request: Req,
) -> Sequence[Res]:
    cache = RequestCache()
    if key in cache:
        return cache[key]

    response = endpoint(request)
    cache[key] = response
    return response


class RequestCache:
    _cache: Dict[str, Sequence[constructs.DataApiConstruct]] = {}

    def __getitem__(self, item):
        return self._cache[item]

    def __setitem__(self, key, value):
        self._cache[key] = value

    def __contains__(self, item):
        return item in self._cache
