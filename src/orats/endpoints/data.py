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
from typing import Any, Iterable, Mapping, Sequence

import httpx

from orats.errors import InsufficientPermissionsError
from orats.model.data import request as req
from orats.model.data import response as res


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


class DataApiEndpoint(abc.ABC):
    """An **Endpoint** handles a **Request** and relays the **Response**."""

    _base_url = "https://api.orats.io/datav2"
    _resource: str
    # Set this to true in subclasses that always use the historical prefix
    _is_historical: bool = False

    def __init__(self, token: str):
        """Initializes an API endpoint for a specified resource.

        Args:
          token:
            The authentication token provided to the user.
        """
        self._token = token

    @abc.abstractmethod
    def __call__(self, request) -> Sequence:
        """Handles a request and relays the response.

        Args:
          request:
            Data API request object.

        Returns:
          One or more Data API response objects.
        """
        ...

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

    def _get(
        self,
        request: req.DataApiRequest,
    ) -> Mapping[str, Any]:
        is_historical = self._is_historical
        if not is_historical and isinstance(request, req.DataHistoryApiRequest):
            is_historical = request.trade_date is not None

        params = self._update_params(request.dict(by_alias=True))
        return _get(
            url=self._url(historical=is_historical),
            params=params,
        )


class TickersEndpoint(DataApiEndpoint):
    _resource = "tickers"

    def __call__(self, request: req.TickersRequest) -> Sequence[res.Ticker]:
        """Retrieves the duration of available data for various assets.

        If no underlying asset is specified, the result will be a list
        of all available ticker symbols. Each symbol is accompanied by
        a start (min) and end (max) date for which data is available.
        See the corresponding `Tickers`_ endpoint.

        Args:
          request:
            Tickers request object.

        Returns:
          A list of tickers with data durations.
        """
        api_response = res.DataApiResponse[res.Ticker](**self._get(request))
        return api_response.data or ()


class StrikesEndpoint(DataApiEndpoint):
    _resource = "strikes"

    def __call__(self, request: req.StrikesRequest) -> Sequence[res.Strike]:
        """Retrieves strikes data for the given asset(s).

        See the corresponding `Strikes`_ and `Strikes History`_ endpoints.

        Args:
          request:
            Strikes request object.

        Returns:
          A list of strikes for each specified asset.
        """

        api_response = res.DataApiResponse[res.Strike](**self._get(request))
        return api_response.data or ()


class StrikesByOptionsEndpoint(DataApiEndpoint):
    _resource = "strikes/options"

    def __call__(
        self,
        *requests: req.StrikesByOptionsRequest,
    ) -> Sequence[res.Strike]:
        """Retrieves strikes data by ticker, expiry, and strike.

        See the corresponding `Strikes by Options`_ and
        `Strikes History by Options`_ endpoints.

        Args:
          requests:
            StrikesByOption request object. Passing a single request will
            use the GET request, while passing a sequence will use the POST
            request method.

        Returns:
          A list of strikes for each specified asset.
        """
        if len(requests) == 1:
            response = self._get(requests[0])
        else:
            response = self._post(requests)

        api_response = res.DataApiResponse[res.Strike](**response)
        return api_response.data or ()

    def _post(
        self, requests: Sequence[req.StrikesByOptionsRequest]
    ) -> Mapping[str, Any]:
        body = [json.loads(request.json(by_alias=True)) for request in requests]
        return _post(url=self._url(), body=body, params=self._update_params({}))


class MoniesImpliedEndpoint(DataApiEndpoint):
    _resource = "monies/implied"

    def __call__(
        self,
        request: req.MoniesRequest,
    ) -> Sequence[res.MoneyImplied]:
        """Retrieves monthly implied data for monies.

        See the corresponding `Monies`_ and `Monies History`_ endpoints.

        Args:
          request:
            Monies request object.

        Returns:
          A list of implied monies for each specified asset.
        """

        api_response = res.DataApiResponse[res.MoneyImplied](**self._get(request))
        return api_response.data or ()


class MoniesForecastEndpoint(DataApiEndpoint):
    _resource = "monies/forecast"

    def __call__(
        self,
        request: req.MoniesRequest,
    ) -> Sequence[res.MoneyForecast]:
        """Retrieves monthly forecast data for monies.

        See the corresponding `Monies`_ and `Monies History`_ endpoints.

        Args:
          request:
            Monies request object.

        Returns:
          A list of forecast monies for each specified asset.
        """

        api_response = res.DataApiResponse[res.MoneyForecast](**self._get(request))
        return api_response.data or ()


class SummariesEndpoint(DataApiEndpoint):
    _resource = "summaries"

    def __call__(
        self,
        request: req.SummariesRequest,
    ) -> Sequence[res.SmvSummary]:
        """Retrieves SMV Summary data.

        See the corresponding `Summaries`_ and `Summaries History`_ endpoints.

        Args:
          request:
            Summaries request object.

        Returns:
          A list of SMV summaries for each specified asset.
        """

        api_response = res.DataApiResponse[res.SmvSummary](**self._get(request))
        return api_response.data or ()


class CoreDataEndpoint(DataApiEndpoint):
    _resource = "cores"

    def __call__(self, request: req.CoreDataRequest) -> Sequence[res.Core]:
        """Retrieves Core data.

        See the corresponding `Core Data`_ and `Core Data History`_ endpoints.

        Args:
          request:
            CoreData request object.

        Returns:
          A list of core data for each specified asset.
        """

        api_response = res.DataApiResponse[res.Core](**self._get(request))
        return api_response.data or ()


class DailyPriceEndpoint(DataApiEndpoint):
    _resource = "dailies"
    _is_historical = True

    def __call__(
        self,
        request: req.DailyPriceRequest,
    ) -> Sequence[res.DailyPrice]:
        """Retrieves end of day daily stock price data.

        See the corresponding `Daily Price`_ endpoint.

        Args:
          request:
            DailyPrice request object.

        Returns:
          A list of daily price data for each specified asset.
        """

        api_response = res.DataApiResponse[res.DailyPrice](**self._get(request))
        return api_response.data or ()


class HistoricalVolatilityEndpoint(DataApiEndpoint):
    _resource = "hvs"
    _is_historical = True

    def __call__(
        self,
        request: req.HistoricalVolatilityRequest,
    ) -> Sequence[res.HistoricalVolatility]:
        """Retrieves historical volatility data.

        See the corresponding `Historical Volatility`_ endpoint.

        Args:
          request:
            HistoricalVolatility request object.

        Returns:
          A list of historical volatility data for each specified asset.
        """

        api_response = res.DataApiResponse[res.HistoricalVolatility](
            **self._get(request)
        )
        return api_response.data or ()


class DividendHistoryEndpoint(DataApiEndpoint):
    _resource = "divs"
    _is_historical = True

    def __call__(
        self,
        request: req.DividendHistoryRequest,
    ) -> Sequence[res.DividendHistory]:
        """Retrieves dividend history data.

        See the corresponding `Dividend History`_ endpoint.

        Args:
          request:
            DividendHistory request object.

        Returns:
          A list of dividend history data for each specified asset.
        """

        api_response = res.DataApiResponse[res.DividendHistory](**self._get(request))
        return api_response.data or ()


class EarningsHistoryEndpoint(DataApiEndpoint):
    _resource = "earnings"
    _is_historical = True

    def __call__(
        self,
        request: req.EarningsHistoryRequest,
    ) -> Sequence[res.EarningsHistory]:
        """Retrieves earnings history data.

        See the corresponding `Earnings History`_ endpoint.

        Args:
          request:
            EarningsHistory request object.

        Returns:
          A list of earnings history data for each specified asset.
        """

        api_response = res.DataApiResponse[res.EarningsHistory](**self._get(request))
        return api_response.data or ()


class StockSplitHistoryEndpoint(DataApiEndpoint):
    _resource = "splits"
    _is_historical = True

    def __call__(
        self,
        request: req.StockSplitHistoryRequest,
    ) -> Sequence[res.StockSplitHistory]:
        """Retrieves stock split history data.

        See the corresponding `Stock Split History`_ endpoint.

        Args:
          request:
            StockSplitHistory request object.

        Returns:
          A list of stock split history data for each specified asset.
        """

        api_response = res.DataApiResponse[res.StockSplitHistory](**self._get(request))
        return api_response.data or ()


class IvRankEndpoint(DataApiEndpoint):
    _resource = "ivrank"

    def __call__(
        self,
        request: req.IvRankRequest,
    ) -> Sequence[res.IvRank]:
        """Retrieves IV rank data.

        See the corresponding `IV Rank`_ and `IV Rank History`_ endpoints.

        Args:
          request:
            IvRank request object.

        Returns:
          A list of IV rank data for each specified asset.
        """

        api_response = res.DataApiResponse[res.IvRank](**self._get(request))
        return api_response.data or ()


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
