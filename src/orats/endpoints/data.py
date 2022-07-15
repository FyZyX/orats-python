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


def _get(url, params) -> Sequence[Mapping[str, Any]]:
    response = httpx.get(
        url=url,
        params=params,
    )
    body = response.json()
    if response.status_code == 403:
        raise InsufficientPermissionsError
    return body["data"]


def _post(url, params, body) -> Sequence[Mapping[str, Any]]:
    response = httpx.post(
        url=url,
        json=body,
        params=params,
    )
    if response.status_code == 403:
        raise InsufficientPermissionsError
    body = response.json()
    return body["data"]


class DataApiEndpoint(abc.ABC):
    _base_url = "https://api.orats.io/datav2"
    _resource: str

    def __init__(self, token: str):
        """Initializes an API endpoint for a specified resource.

        Args:
          token:
            The authentication token provided to the user.
        """
        self._token = token

    @abc.abstractmethod
    def __call__(self, request) -> Sequence:
        ...

    def _url(self) -> str:
        return "/".join((self._base_url, self._resource))

    def _update_params(self, params: Mapping[str, Any]) -> Mapping[str, Any]:
        updated_params = dict(token=self._token)
        for key, param in params.items():
            if param is None:
                continue
            if not isinstance(param, str) and isinstance(param, Iterable):
                param = ",".join([str(v) for v in param])
            updated_params[key] = param
        return updated_params

    def _get(self, request: req.DataApiRequest) -> Sequence[Mapping[str, Any]]:
        params = self._update_params(request.dict(by_alias=True))
        return _get(
            url=self._url(),
            params=params,
        )


class TickersEndpoint(DataApiEndpoint):
    _resource = "tickers"

    def __call__(self, request: req.TickersRequest) -> Sequence[res.TickerResponse]:
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
        return [res.TickerResponse(**v) for v in self._get(request)]


class StrikesEndpoint(DataApiEndpoint):
    _resource = "strikes"

    def __call__(self, request: req.StrikesRequest) -> Sequence[res.StrikeResponse]:
        """Retrieves strikes data for the given asset(s).

        See the corresponding `Strikes`_ endpoint.

        Args:
          request:
            Strikes request object.

        Returns:
          A list of strikes for each specified asset.
        """
        return [res.StrikeResponse(**v) for v in self._get(request)]


class StrikesHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/strikes"

    def __call__(
        self, request: req.StrikesHistoryRequest
    ) -> Sequence[res.StrikeResponse]:
        """Retrieves historical strikes data for the given asset(s).

        See the corresponding `Strikes History`_ endpoints.

        Args:
          request:
            StrikesHistory request object.

        Returns:
          A list of historical strikes for each specified asset.
        """
        return [res.StrikeResponse(**v) for v in self._get(request)]


class StrikesByOptionsEndpoint(DataApiEndpoint):
    _resource = "strikes/options"

    def __call__(
        self,
        *requests: req.StrikesByOptionsRequest,
    ) -> Sequence[res.StrikeResponse]:
        """Retrieves strikes data by ticker, expiry, and strike.

        See the corresponding `Strikes by Options`_ endpoint.

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
        return [res.StrikeResponse(**v) for v in response]

    def _post(
        self, requests: Sequence[req.StrikesByOptionsRequest]
    ) -> Sequence[Mapping[str, Any]]:
        body = [json.loads(request.json(by_alias=True)) for request in requests]
        return _post(url=self._url(), body=body, params=self._update_params({}))


class StrikesHistoryByOptionsEndpoint(StrikesByOptionsEndpoint):
    _resource = "hist/strikes/options"

    def __call__(
        self,
        *requests: req.StrikesHistoryByOptionsRequest,
    ) -> Sequence[res.StrikeResponse]:
        """Retrieves historical strikes data by ticker, expiry, and strike.

        See the corresponding `Strikes History by Options`_ endpoint.

        Args:
          request:
            StrikesHistoryByOption request object.

        Returns:
          A list of historical strikes for each specified asset.
        """
        return super().__call__(*requests)


class MoniesImpliedEndpoint(DataApiEndpoint):
    _resource = "monies/implied"

    def __call__(
        self,
        request: req.MoniesRequest,
    ) -> Sequence[res.MoneyImpliedResponse]:
        """Retrieves monthly implied data for monies.

        See the corresponding `Monies`_ endpoint.

        Args:
          request:
            Monies request object.

        Returns:
          A list of implied monies for each specified asset.
        """
        return [res.MoneyImpliedResponse(**v) for v in self._get(request)]


class MoniesImpliedHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/monies/implied"

    def __call__(
        self,
        request: req.MoniesHistoryRequest,
    ) -> Sequence[res.MoneyImpliedResponse]:
        """Retrieves historical monthly implied data for monies.

        See the corresponding `Monies History`_ endpoint.

        Args:
          request:
            MoniesHistory request object.

        Returns:
          A list of historical implied monies for each specified asset.
        """
        return [res.MoneyImpliedResponse(**v) for v in self._get(request)]


class MoniesForecastEndpoint(DataApiEndpoint):
    _resource = "monies/forecast"

    def __call__(
        self,
        request: req.MoniesRequest,
    ) -> Sequence[res.MoneyForecastResponse]:
        """Retrieves monthly forecast data for monies.

        See the corresponding `Monies`_ endpoint.

        Args:
          request:
            Monies request object.

        Returns:
          A list of forecast monies for each specified asset.
        """
        return [res.MoneyForecastResponse(**v) for v in self._get(request)]


class MoniesForecastHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/monies/forecast"

    def __call__(
        self,
        request: req.MoniesHistoryRequest,
    ) -> Sequence[res.MoneyForecastResponse]:
        """Retrieves historical monthly forecast data for monies.

        See the corresponding `Monies History`_ endpoint.

        Args:
          request:
            MoniesHistory request object.

        Returns:
          A list of historical forecast monies for each specified asset.
        """
        return [res.MoneyForecastResponse(**v) for v in self._get(request)]


class SummariesEndpoint(DataApiEndpoint):
    _resource = "summaries"

    def __call__(
        self,
        request: req.SummariesRequest,
    ) -> Sequence[res.SmvSummaryResponse]:
        """Retrieves SMV Summary data.

        See the corresponding `Summaries`_ endpoint.

        Args:
          request:
            Summaries request object.

        Returns:
          A list of SMV summaries for each specified asset.
        """
        return [res.SmvSummaryResponse(**v) for v in self._get(request)]


class SummariesHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/summaries"

    def __call__(
        self,
        request: req.SummariesHistoryRequest,
    ) -> Sequence[res.SmvSummaryResponse]:
        """Retrieves historical SMV Summary data.

        See the corresponding `Summaries History`_ endpoints.

        Args:
          request:
            SummariesHistory request object.

        Returns:
          A list of historical SMV summaries for each specified asset.
        """
        return [res.SmvSummaryResponse(**v) for v in self._get(request)]


class CoreDataEndpoint(DataApiEndpoint):
    _resource = "cores"

    def __call__(self, request: req.CoreDataRequest) -> Sequence[res.CoreResponse]:
        """Retrieves Core data.

        See the corresponding `Core Data`_ endpoint.

        Args:
          request:
            CoreData request object.

        Returns:
          A list of core data for each specified asset.
        """
        return [res.CoreResponse(**v) for v in self._get(request)]


class CoreDataHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/cores"

    def __call__(
        self,
        request: req.CoreDataHistoryRequest,
    ) -> Sequence[res.CoreResponse]:
        """Retrieves historical Core data.

        See the corresponding `Core Data History`_ endpoint.

        Args:
          request:
            CoreDataHistory request object.

        Returns:
          A list of historical core data for each specified asset.
        """
        return [res.CoreResponse(**v) for v in self._get(request)]


class DailyPriceEndpoint(DataApiEndpoint):
    _resource = "hist/dailies"

    def __call__(
        self,
        request: req.DailyPriceRequest,
    ) -> Sequence[res.DailyPriceResponse]:
        """Retrieves end of day daily stock price data.

        See the corresponding `Daily Price`_ endpoint.

        Args:
          request:
            DailyPrice request object.

        Returns:
          A list of daily price data for each specified asset.
        """
        return [res.DailyPriceResponse(**v) for v in self._get(request)]


class HistoricalVolatilityEndpoint(DataApiEndpoint):
    _resource = "hist/hvs"

    def __call__(
        self,
        request: req.HistoricalVolatilityRequest,
    ) -> Sequence[res.HistoricalVolatilityResponse]:
        """Retrieves historical volatility data.

        See the corresponding `Historical Volatility`_ endpoint.

        Args:
          request:
            HistoricalVolatility request object.

        Returns:
          A list of historical volatility data for each specified asset.
        """
        return [res.HistoricalVolatilityResponse(**v) for v in self._get(request)]


class DividendHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/divs"

    def __call__(
        self,
        request: req.DividendHistoryRequest,
    ) -> Sequence[res.DividendHistoryResponse]:
        """Retrieves dividend history data.

        See the corresponding `Dividend History`_ endpoint.

        Args:
          request:
            DividendHistory request object.

        Returns:
          A list of dividend history data for each specified asset.
        """
        return [res.DividendHistoryResponse(**v) for v in self._get(request)]


class EarningsHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/earnings"

    def __call__(
        self,
        request: req.EarningsHistoryRequest,
    ) -> Sequence[res.EarningsHistoryResponse]:
        """Retrieves earnings history data.

        See the corresponding `Earnings History`_ endpoint.

        Args:
          request:
            EarningsHistory request object.

        Returns:
          A list of earnings history data for each specified asset.
        """
        return [res.EarningsHistoryResponse(**v) for v in self._get(request)]


class StockSplitHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/splits"

    def __call__(
        self,
        request: req.StockSplitHistoryRequest,
    ) -> Sequence[res.StockSplitHistoryResponse]:
        """Retrieves stock split history data.

        See the corresponding `Stock Split History`_ endpoint.

        Args:
          request:
            StockSplitHistory request object.

        Returns:
          A list of stock split history data for each specified asset.
        """
        return [res.StockSplitHistoryResponse(**v) for v in self._get(request)]


class IvRankEndpoint(DataApiEndpoint):
    _resource = "ivrank"

    def __call__(
        self,
        request: req.IvRankRequest,
    ) -> Sequence[res.IvRankResponse]:
        """Retrieves IV rank data.

        See the corresponding `IV Rank`_ endpoint.

        Args:
          request:
            IvRank request object.

        Returns:
          A list of IV rank data for each specified asset.
        """
        return [res.IvRankResponse(**v) for v in self._get(request)]


class IvRankHistoryEndpoint(DataApiEndpoint):
    _resource = "hist/ivrank"

    def __call__(
        self,
        request: req.IvRankHistoryRequest,
    ) -> Sequence[res.IvRankResponse]:
        """Retrieves historical IV rank data.

        See the corresponding `IV Rank History`_ endpoint.

        Args:
          request:
            IvRankHistory request object.

        Returns:
          A list of historical IV rank data for each specified asset.
        """
        return [res.IvRankResponse(**v) for v in self._get(request)]


class DataApi:
    """Low-level interface to the `Data API`_.

    A direct translation of the Data API that simply wraps the
    responses in structured Python objects.
    """

    def __init__(self, token: str):
        self.tickers = TickersEndpoint(token)
        self.strikes = StrikesEndpoint(token)
        self.strikes_history = StrikesHistoryEndpoint(token)
        self.strikes_by_options = StrikesByOptionsEndpoint(token)
        self.strikes_history_by_options = StrikesHistoryByOptionsEndpoint(token)
        self.monies_implied = MoniesImpliedEndpoint(token)
        self.monies_implied_history = MoniesImpliedHistoryEndpoint(token)
        self.monies_forecast = MoniesForecastEndpoint(token)
        self.monies_forecast_history = MoniesForecastHistoryEndpoint(token)
        self.summaries = SummariesEndpoint(token)
        self.summaries_history = SummariesHistoryEndpoint(token)
        self.core_data = CoreDataEndpoint(token)
        self.core_data_history = CoreDataHistoryEndpoint(token)
        self.daily_price = DailyPriceEndpoint(token)
        self.historical_volatility = HistoricalVolatilityEndpoint(token)
        self.dividend_history = DividendHistoryEndpoint(token)
        self.earnings_history = EarningsHistoryEndpoint(token)
        self.stock_split_history = StockSplitHistoryEndpoint(token)
        self.iv_rank = IvRankEndpoint(token)
        self.iv_rank_history = IvRankHistoryEndpoint(token)
