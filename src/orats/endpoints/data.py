"""ORATS Data API.

Primary features include

* historical options data
* historical volatilities
* greeks
* bid/ask quotes
* 100+ indicators

See the `product page`_ and `API docs`_.

.. _product page: https://orats.com/data-api/
.. _API docs: https://docs.orats.io/datav2-api-guide/
"""
import json
from typing import Any, Iterable, Generic, Mapping, Sequence, Type, TypeAlias, TypeVar

import httpx

from orats.errors import InsufficientPermissionsError
from orats.constructs.api.data import request as req
from orats.constructs.api.data import response as res


def _handle_response(response: httpx.Response) -> Mapping[str, Any]:
    if response.status_code == 403:
        raise InsufficientPermissionsError
    return response.json()


def _get(url, params) -> Mapping[str, Any]:
    response = httpx.get(
        url=url,
        params=params,
    )
    return _handle_response(response)


def _post(url, params, body) -> Mapping[str, Any]:
    response = httpx.post(
        url=url,
        json=body,
        params=params,
    )
    return _handle_response(response)


Req = TypeVar("Req", bound=req.DataApiRequest)
Res = TypeVar("Res", bound=res.DataApiConstruct)


class DataApiEndpoint(Generic[Req, Res]):
    """An endpoint handles a request and relays the response."""

    _base_url = "https://api.orats.io/datav2"
    _resource: str
    # This is a workaround to get access to the specific construct type
    _response_type: Type[Res]
    # Set this to true in subclasses that always use the historical prefix
    _is_historical: bool = False

    def __init__(self, token: str):
        """Initializes an API endpoint for a specified resource.

        Args:
          token:
            The authentication token provided to the user.
        """
        self._token = token

    def __call__(self, request: Req) -> Sequence[Res]:
        """Handles a request and relays the response.

        Args:
          request:
            Data API request object.

        Returns:
          One or more Data API response objects.
        """
        response = res.DataApiResponse[self._response_type](  # type: ignore
            **self._get(request)
        )
        return response.data or ()

    def _url(self, historical: bool = False) -> str:
        resource = self._resource
        if historical:
            resource = f"hist/{resource}"

        return "/".join((self._base_url, resource))

    def _update_params(self, params: Mapping[str, Any]) -> Mapping[str, Any]:
        updated_params = dict(token=self._token)
        for key, param in params.items():
            if param is None:
                continue
            if not isinstance(param, str) and isinstance(param, Iterable):
                param = ",".join([str(v) for v in param])
            updated_params[key] = param
        return updated_params

    def _get(self, request: Req) -> Mapping[str, Any]:
        is_historical = self._is_historical
        if not is_historical and isinstance(request, req.DataHistoryApiRequest):
            is_historical = request.trade_date is not None

        params = self._update_params(request.dict(by_alias=True))
        return _get(
            url=self._url(historical=is_historical),
            params=params,
        )


class TickersEndpoint(DataApiEndpoint[req.TickersRequest, res.Ticker]):
    """Retrieves the duration of available data for various assets.

    If no underlying asset is specified, the result will be a list
    of all available ticker symbols. Each symbol is accompanied by
    a start (min) and end (max) date for which data is available.
    See the corresponding `Tickers`_ endpoint.
    """

    _resource = "tickers"
    _response_type = res.Ticker


class StrikesEndpoint(DataApiEndpoint[req.StrikesRequest, res.Strike]):
    """Retrieves strikes data for the given asset(s).

    See the corresponding `Strikes`_ and `Strikes History`_ endpoints.
    """

    _resource = "strikes"
    _response_type = res.Strike


class StrikesByOptionsEndpoint(
    DataApiEndpoint[req.StrikesByOptionsRequest, res.Strike]
):
    """Retrieves strikes data by ticker, expiry, and strike.

    See the corresponding `Strikes by Options`_ and
    `Strikes History by Options`_ endpoints.
    """

    _resource = "strikes/options"
    _response_type = res.Strike

    def __call__(
        self,
        *requests: req.StrikesByOptionsRequest,
    ) -> Sequence[res.Strike]:
        """Makes a call to the appropriate API endpoint.

        Passing a single request will use the GET request method,
        while passing a sequence will use the POST request method.

        Args:
          requests:
            StrikesByOption request object.

        Returns:
          A list of strikes for each specified asset.
        """
        if len(requests) == 1:
            return super().__call__(requests[0])
        else:
            response = res.DataApiResponse[self._response_type](  # type: ignore
                **self._post(requests)
            )
            return response.data or ()

    def _post(
        self, requests: Sequence[req.StrikesByOptionsRequest]
    ) -> Mapping[str, Any]:
        body = [json.loads(request.json(by_alias=True)) for request in requests]
        return _post(url=self._url(), body=body, params=self._update_params({}))


class MoniesImpliedEndpoint(DataApiEndpoint[req.MoniesRequest, res.MoneyImplied]):
    """Retrieves monthly implied data for monies.

    See the corresponding `Monies`_ and `Monies History`_ endpoints.
    """

    _resource = "monies/implied"
    _response_type = res.MoneyImplied


class MoniesForecastEndpoint(DataApiEndpoint[req.MoniesRequest, res.MoneyForecast]):
    """Retrieves monthly forecast data for monies.

    See the corresponding `Monies`_ and `Monies History`_ endpoints.
    """

    _resource = "monies/forecast"
    _response_type = res.MoneyForecast


class SummariesEndpoint(DataApiEndpoint[req.SummariesRequest, res.SmvSummary]):
    """Retrieves SMV Summary data.

    See the corresponding `Summaries`_ and `Summaries History`_ endpoints.
    """

    _resource = "summaries"
    _response_type = res.SmvSummary


class CoreDataEndpoint(DataApiEndpoint):
    """Retrieves Core data.

    See the corresponding `Core Data`_ and `Core Data History`_ endpoints.
    """

    _resource = "cores"
    _response_type = res.Core


class DailyPriceEndpoint(DataApiEndpoint[req.DailyPriceRequest, res.DailyPrice]):
    """Retrieves end of day daily stock price data.

    See the corresponding `Daily Price`_ endpoint.
    """

    _resource = "dailies"
    _response_type = res.DailyPrice
    _is_historical = True


class HistoricalVolatilityEndpoint(
    DataApiEndpoint[req.HistoricalVolatilityRequest, res.HistoricalVolatility]
):
    """Retrieves historical volatility data.

    See the corresponding `Historical Volatility`_ endpoint.
    """

    _resource = "hvs"
    _response_type = res.HistoricalVolatility
    _is_historical = True


class DividendHistoryEndpoint(
    DataApiEndpoint[req.DividendHistoryRequest, res.DividendHistory]
):
    """Retrieves dividend history data.

    See the corresponding `Dividend History`_ endpoint.
    """

    _resource = "divs"
    _response_type = res.DividendHistory
    _is_historical = True


class EarningsHistoryEndpoint(
    DataApiEndpoint[req.EarningsHistoryRequest, res.EarningsHistory]
):
    """Retrieves earnings history data.

    See the corresponding `Earnings History`_ endpoint.
    """

    _resource = "earnings"
    _response_type = res.EarningsHistory
    _is_historical = True


class StockSplitHistoryEndpoint(
    DataApiEndpoint[req.StockSplitHistoryRequest, res.StockSplitHistory]
):
    """Retrieves stock split history data.

    See the corresponding `Stock Split History`_ endpoint.
    """

    _resource = "splits"
    _response_type = res.StockSplitHistory
    _is_historical = True


class IvRankEndpoint(DataApiEndpoint[req.IvRankRequest, res.IvRank]):
    """Retrieves IV rank data.

    See the corresponding `IV Rank`_ and `IV Rank History`_ endpoints.
    """

    _resource = "ivrank"
    _response_type = res.IvRank


class DataApi:
    """Low-level interface to the `Data API`_.

    A direct translation of the Data API that simply wraps the
    responses in structured Python objects.
    """

    def __init__(self, token: str):
        self.tickers = TickersEndpoint(token)
        self.strikes = StrikesEndpoint(token)
        self.strikes_by_options = StrikesByOptionsEndpoint(token)
        self.monies_implied = MoniesImpliedEndpoint(token)
        self.monies_forecast = MoniesForecastEndpoint(token)
        self.summaries = SummariesEndpoint(token)
        self.core_data = CoreDataEndpoint(token)
        self.daily_price = DailyPriceEndpoint(token)
        self.historical_volatility = HistoricalVolatilityEndpoint(token)
        self.dividend_history = DividendHistoryEndpoint(token)
        self.earnings_history = EarningsHistoryEndpoint(token)
        self.stock_split_history = StockSplitHistoryEndpoint(token)
        self.iv_rank = IvRankEndpoint(token)
