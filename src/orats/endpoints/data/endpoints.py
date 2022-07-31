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
import abc
import json
from typing import Any, Iterable, Generic, Mapping, Sequence, Type, TypeVar, Callable

import httpx

from orats.common import get_token
from orats.constructs.api import data as api_constructs
from orats.endpoints import common
from orats.endpoints.data import request as req, response as res
from orats.endpoints.data.cache import RequestCache
from orats.endpoints.data.generator import FakeDataGenerator
from orats.errors import InsufficientPermissionsError


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
Res = TypeVar("Res", bound=api_constructs.DataApiConstruct)


class DataApiEndpoint(abc.ABC, Generic[Req, Res]):
    """An endpoint handles a request and relays the response."""

    _base_url = "https://api.orats.io/datav2"
    _resource: str
    # This is a workaround to get access to the specific construct type
    _response_type: Type[Res]
    # Set this to true in subclasses that always use the historical prefix
    _is_historical: bool = False
    _cache = RequestCache()
    _data_generator = FakeDataGenerator()

    def __init__(self, token: str = None, mock: bool = False):
        """Initializes an API endpoint for a specified resource.

        Args:
          token:
            The authentication token provided to the user.
        """
        self._token = token or get_token()
        self._mock = mock

    def __call__(self, request: Req) -> Sequence[Res]:
        """Handles a request and relays the response.

        Args:
          request:
            Data API request object.

        Returns:
          One or more Data API response objects.
        """
        if self._mock:
            return self._generate_fake_data(request)  # type: ignore

        key = self._key(*request.dict().values())
        if key in self._cache:
            return self._cache[key]

        response = res.DataApiResponse[self._response_type](  # type: ignore
            **self._get(request)
        )
        data = response.data or ()
        self._cache[key] = data
        return data

    def _key(self, *components):
        return f"{self._resource}-{'-'.join([str(c) for c in components])}"

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

    @abc.abstractmethod
    def _generate_fake_data(self, request: Req) -> Sequence[Res]:
        pass


class TickersEndpoint(DataApiEndpoint[req.TickersRequest, api_constructs.Ticker]):
    """Retrieves the duration of available data for various assets.

    If no underlying asset is specified, the result will be a list
    of all available ticker symbols. Each symbol is accompanied by
    a start (min) and end (max) date for which data is available.
    See the corresponding `Tickers`_ endpoint.
    """

    _resource = "tickers"
    _response_type = api_constructs.Ticker

    def _generate_fake_data(
        self, request: req.TickersRequest
    ) -> Sequence[api_constructs.Ticker]:
        universe = [request.ticker] if request.ticker else common.universe()
        results = [self._data_generator.ticker(ticker) for ticker in universe]
        return common.as_responses(api_constructs.Ticker, results)


class StrikesEndpoint(DataApiEndpoint[req.StrikesRequest, api_constructs.Strike]):
    """Retrieves strikes data for the given asset(s).

    See the corresponding `Strikes`_ and `Strikes History`_ endpoints.
    """

    _resource = "strikes"
    _response_type = api_constructs.Strike

    def _generate_fake_data(
        self, request: req.StrikesRequest
    ) -> Sequence[api_constructs.Strike]:
        universe = request.tickers or common.universe()
        results = [self._data_generator.strike(ticker) for ticker in universe]
        return common.as_responses(api_constructs.Strike, results)


class StrikesByOptionsEndpoint(
    DataApiEndpoint[req.StrikesByOptionsRequest, api_constructs.Strike]
):
    """Retrieves strikes data by ticker, expiry, and strike.

    See the corresponding `Strikes by Options`_ and
    `Strikes History by Options`_ endpoints.
    """

    _resource = "strikes/options"
    _response_type = api_constructs.Strike

    def __call__(
        self,
        *requests: req.StrikesByOptionsRequest,
    ) -> Sequence[api_constructs.Strike]:
        """Makes a call to the appropriate API endpoint.

        Passing a single request will use the GET request method,
        while passing a sequence will use the POST request method.

        Args:
          requests:
            StrikesByOption request object.

        Returns:
          A list of strikes for each specified asset.
        """
        if self._mock:
            return self._generate_fake_data(*requests)

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

    def _generate_fake_data(
        self, *requests: req.StrikesByOptionsRequest
    ) -> Sequence[api_constructs.Strike]:
        results = [self._data_generator.strike(request.ticker) for request in requests]
        return common.as_responses(api_constructs.Strike, results)


class MoniesImpliedEndpoint(
    DataApiEndpoint[req.MoniesRequest, api_constructs.MoneyImplied]
):
    """Retrieves monthly implied data for monies.

    See the corresponding `Monies`_ and `Monies History`_ endpoints.
    """

    _resource = "monies/implied"
    _response_type = api_constructs.MoneyImplied

    def _generate_fake_data(
        self, request: req.MoniesRequest
    ) -> Sequence[api_constructs.MoneyImplied]:
        universe = request.tickers or common.universe()
        monies = []
        for ticker in universe:
            results = [
                self._data_generator.money_implied(ticker, days_to_expiration=dte)
                for dte in range(1, 100, 7)
            ]
            monies.extend(common.as_responses(api_constructs.MoneyImplied, results))
        return monies


class MoniesForecastEndpoint(
    DataApiEndpoint[req.MoniesRequest, api_constructs.MoneyForecast]
):
    """Retrieves monthly forecast data for monies.

    See the corresponding `Monies`_ and `Monies History`_ endpoints.
    """

    _resource = "monies/forecast"
    _response_type = api_constructs.MoneyForecast

    def _generate_fake_data(
        self, request: req.MoniesRequest
    ) -> Sequence[api_constructs.MoneyForecast]:
        universe = request.tickers or common.universe()
        monies = []
        for ticker in universe:
            results = [
                self._data_generator.money_forecast(ticker, days_to_expiration=dte)
                for dte in range(1, 100, 7)
            ]
            monies.extend(common.as_responses(api_constructs.MoneyForecast, results))
        return monies


class SummariesEndpoint(DataApiEndpoint[req.SummariesRequest, api_constructs.Summary]):
    """Retrieves SMV Summary data.

    See the corresponding `Summaries`_ and `Summaries History`_ endpoints.
    """

    _resource = "summaries"
    _response_type = api_constructs.Summary

    def _generate_fake_data(
        self, request: req.SummariesRequest
    ) -> Sequence[api_constructs.Summary]:
        universe = request.tickers or common.universe()
        results = [self._data_generator.summary(ticker) for ticker in universe]
        return common.as_responses(api_constructs.Summary, results)


class CoreDataEndpoint(DataApiEndpoint[req.CoreDataRequest, api_constructs.Core]):
    """Retrieves Core data.

    See the corresponding `Core Data`_ and `Core Data History`_ endpoints.
    """

    _resource = "cores"
    _response_type = api_constructs.Core

    def _generate_fake_data(
        self, request: req.CoreDataRequest
    ) -> Sequence[api_constructs.Core]:
        universe = request.tickers or common.universe()
        results = [self._data_generator.core(ticker) for ticker in universe]
        return common.as_responses(api_constructs.Core, results)


class DailyPriceEndpoint(
    DataApiEndpoint[req.DailyPriceRequest, api_constructs.DailyPrice]
):
    """Retrieves end of day daily stock price data.

    See the corresponding `Daily Price`_ endpoint.
    """

    _resource = "dailies"
    _response_type = api_constructs.DailyPrice
    _is_historical = True

    def _generate_fake_data(
        self, request: req.DailyPriceRequest
    ) -> Sequence[api_constructs.DailyPrice]:
        universe = request.tickers or common.universe()
        results = [self._data_generator.daily_price(ticker) for ticker in universe]
        return common.as_responses(api_constructs.DailyPrice, results)


class HistoricalVolatilityEndpoint(
    DataApiEndpoint[
        req.HistoricalVolatilityRequest, api_constructs.HistoricalVolatility
    ]
):
    """Retrieves historical volatility data.

    See the corresponding `Historical Volatility`_ endpoint.
    """

    _resource = "hvs"
    _response_type = api_constructs.HistoricalVolatility
    _is_historical = True

    def _generate_fake_data(
        self, request: req.HistoricalVolatilityRequest
    ) -> Sequence[api_constructs.HistoricalVolatility]:
        universe = request.tickers or common.universe()
        results = [
            self._data_generator.historical_volatility(ticker) for ticker in universe
        ]
        return common.as_responses(api_constructs.HistoricalVolatility, results)


class DividendHistoryEndpoint(
    DataApiEndpoint[req.DividendHistoryRequest, api_constructs.DividendHistory]
):
    """Retrieves dividend history data.

    See the corresponding `Dividend History`_ endpoint.
    """

    _resource = "divs"
    _response_type = api_constructs.DividendHistory
    _is_historical = True

    def _generate_fake_data(
        self, request: req.DividendHistoryRequest
    ) -> Sequence[api_constructs.DividendHistory]:
        universe = [request.ticker] if request.ticker else common.universe()
        results = [self._data_generator.dividend_history(ticker) for ticker in universe]
        return common.as_responses(api_constructs.DividendHistory, results)


class EarningsHistoryEndpoint(
    DataApiEndpoint[req.EarningsHistoryRequest, api_constructs.EarningsHistory]
):
    """Retrieves earnings history data.

    See the corresponding `Earnings History`_ endpoint.
    """

    _resource = "earnings"
    _response_type = api_constructs.EarningsHistory
    _is_historical = True

    def _generate_fake_data(
        self, request: req.EarningsHistoryRequest
    ) -> Sequence[api_constructs.EarningsHistory]:
        universe = [request.ticker] if request.ticker else common.universe()
        results = [self._data_generator.earnings_history(ticker) for ticker in universe]
        return common.as_responses(api_constructs.EarningsHistory, results)


class StockSplitHistoryEndpoint(
    DataApiEndpoint[req.StockSplitHistoryRequest, api_constructs.StockSplitHistory]
):
    """Retrieves stock split history data.

    See the corresponding `Stock Split History`_ endpoint.
    """

    _resource = "splits"
    _response_type = api_constructs.StockSplitHistory
    _is_historical = True

    def _generate_fake_data(
        self, request: req.StockSplitHistoryRequest
    ) -> Sequence[api_constructs.StockSplitHistory]:
        universe = [request.ticker] if request.ticker else common.universe()
        results = [
            self._data_generator.stock_split_history(ticker) for ticker in universe
        ]
        return common.as_responses(api_constructs.StockSplitHistory, results)


class IvRankEndpoint(DataApiEndpoint[req.IvRankRequest, api_constructs.IvRank]):
    """Retrieves IV rank data.

    See the corresponding `IV Rank`_ and `IV Rank History`_ endpoints.
    """

    _resource = "ivrank"
    _response_type = api_constructs.IvRank

    def _generate_fake_data(
        self, request: req.IvRankRequest
    ) -> Sequence[api_constructs.IvRank]:
        universe = request.tickers or common.universe()
        results = [self._data_generator.iv_rank(ticker) for ticker in universe]
        return common.as_responses(api_constructs.IvRank, results)
