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

from typing import Any, Iterable, Mapping, Sequence

import httpx

from orats.errors import UnauthorizedUserError
from orats.model.data import request as req
from orats.model.data import response as res


class DataApiEndpoint:
    _base_url = "https://api.orats.io/datav2"

    def __init__(self, token: str):
        """Initializes an API interface from configuration.

        Each API call requires a token for authentication.
        This token is supplied to the instance to facilitate
        the use of multiple instances utilizing different tokens.

        Args:
          token:
            The authentication token provided to the user.
        """
        self._token = token

    def _url(self, path: str):
        return "/".join((self._base_url, path))

    def _update_params(self, params: Mapping[str, Any]):
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
        path: str,
        **params: Any,
    ):
        response = httpx.get(
            url=self._url(path),
            params=self._update_params(params),
        )
        body = response.json()
        if response.status_code == 403:
            raise UnauthorizedUserError
        return body["data"]


class TickersEndpoint(DataApiEndpoint):
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
        data = self._get("tickers", **request.dict(by_alias=True))
        return [res.TickerResponse(**t) for t in data]


class StrikesEndpoint(DataApiEndpoint):
    def __call__(self, request: req.StrikesRequest) -> Sequence[res.StrikeResponse]:
        """Retrieves strikes data for the given asset(s).

        See the corresponding `Strikes`_ endpoint.

        Args:
          request:
            Strikes request object.

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get("strikes", **request.dict(by_alias=True))
        return [res.StrikeResponse(**s) for s in data]


class StrikesHistoryEndpoint(DataApiEndpoint):
    def __call__(
        self, request: req.StrikesHistoryRequest
    ) -> Sequence[res.StrikeResponse]:
        """Retrieves historical strikes data for the given asset(s).

        See the corresponding `Strikes History`_ endpoints.

        Args:
          request:
            StrikesHistory request object.

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get("hist/strikes", **request.dict(by_alias=True))
        return [res.StrikeResponse(**s) for s in data]


class StrikesByOptionsEndpoint(DataApiEndpoint):
    def __call__(
        self,
        request: req.StrikesByOptionsRequest,
    ) -> Sequence[res.StrikeResponse]:
        """Retrieves strikes data by ticker, expiry, and strike.

        See the corresponding `Strikes by Options`_ endpoint.

        Args:
          request:
            StrikesByOption request object.

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get("strikes/options", **request.dict(by_alias=True))
        return [res.StrikeResponse(**s) for s in data]


class StrikesHistoryByOptionsEndpoint(DataApiEndpoint):
    def __call__(
        self,
        request: req.StrikesHistoryByOptionsRequest,
    ) -> Sequence[res.StrikeResponse]:
        """Retrieves historical strikes data by ticker, expiry, and strike.

        See the corresponding `Strikes History by Options`_ endpoint.

        Args:
          request:
            StrikesHistoryByOption request object.

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get("hist/strikes/options", **request.dict(by_alias=True))
        return [res.StrikeResponse(**s) for s in data]


class MoniesImpliedEndpoint(DataApiEndpoint):
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
        data = self._get("monies/implied", **request.dict(by_alias=True))
        return [res.MoneyImpliedResponse(**m) for m in data]


class MoniesImpliedHistoryEndpoint(DataApiEndpoint):
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
          A list of implied monies for each specified asset.
        """
        data = self._get("hist/monies/implied", **request.dict(by_alias=True))
        return [res.MoneyImpliedResponse(**m) for m in data]


class MoniesForecastEndpoint(DataApiEndpoint):
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
        data = self._get("monies/forecast", **request.dict(by_alias=True))
        return [res.MoneyForecastResponse(**m) for m in data]


class MoniesForecastHistoryEndpoint(DataApiEndpoint):
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
          A list of forecast monies for each specified asset.
        """
        data = self._get("hist/monies/forecast", **request.dict(by_alias=True))
        return [res.MoneyForecastResponse(**m) for m in data]


class SummariesEndpoint(DataApiEndpoint):
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
        data = self._get("summaries", **request.dict(by_alias=True))
        return [res.SmvSummaryResponse(**m) for m in data]


class SummariesHistoryEndpoint(DataApiEndpoint):
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
          A list of SMV summaries for each specified asset.
        """
        data = self._get("hist/summaries", **request.dict(by_alias=True))
        return [res.SmvSummaryResponse(**m) for m in data]


class CoreDataEndpoint(DataApiEndpoint):
    def __call__(self, request: req.CoreDataRequest) -> Sequence[res.CoreResponse]:
        """Retrieves Core data.

        See the corresponding `Core Data`_ endpoint.

        Args:
          request:
            CoreData request object.

        Returns:
          A list of core data for each specified asset.
        """
        data = self._get("cores", **request.dict(by_alias=True))
        return [res.CoreResponse(**c) for c in data]


class CoreDataHistoryEndpoint(DataApiEndpoint):
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
          A list of core data for each specified asset.
        """
        data = self._get("hist/cores", **request.dict(by_alias=True))
        return [res.CoreResponse(**c) for c in data]


class DailyPriceEndpoint(DataApiEndpoint):
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
        data = self._get("hist/dailies", **request.dict(by_alias=True))
        return [res.DailyPriceResponse(**p) for p in data]


class HistoricalVolatilityEndpoint(DataApiEndpoint):
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
        data = self._get("hist/hvs", **request.dict(by_alias=True))
        return [res.HistoricalVolatilityResponse(**hv) for hv in data]


class DividendHistoryEndpoint(DataApiEndpoint):
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
        data = self._get("hist/divs", **request.dict(by_alias=True))
        return [res.DividendHistoryResponse(**d) for d in data]


class EarningsHistoryEndpoint(DataApiEndpoint):
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
        data = self._get("hist/earnings", **request.dict(by_alias=True))
        return [res.EarningsHistoryResponse(**e) for e in data]


class StockSplitHistoryEndpoint(DataApiEndpoint):
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
        data = self._get("hist/splits", **request.dict(by_alias=True))
        return [res.StockSplitHistoryResponse(**e) for e in data]


class IvRankEndpoint(DataApiEndpoint):
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
          A list of IV rank history data for each specified asset.
        """
        data = self._get("ivrank", **request.dict(by_alias=True))
        return [res.IvRankResponse(**e) for e in data]


class IvRankHistoryEndpoint(DataApiEndpoint):
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
          A list of IV rank history data for each specified asset.
        """
        data = self._get("hist/ivrank", **request.dict(by_alias=True))
        return [res.IvRankResponse(**e) for e in data]


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
        self.core_date = CoreDataEndpoint(token)
        self.core_data_history = CoreDataHistoryEndpoint(token)
        self.daily_price = DailyPriceEndpoint(token)
        self.historical_volatility = HistoricalVolatilityEndpoint(token)
        self.dividend_history = DividendHistoryEndpoint(token)
        self.earnings_history = EarningsHistoryEndpoint(token)
        self.stock_split_history = StockSplitHistoryEndpoint(token)
        self.iv_rank = IvRankEndpoint(token)
        self.iv_rank_history = IvRankHistoryEndpoint(token)
