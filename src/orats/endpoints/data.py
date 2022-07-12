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

from orats.errors import InsufficientPermissionsError
from orats.model.data import request as req
from orats.model.data import response as res


class DataApi:
    """Low-level interface to the `Data API`_.

    A direct translation of the Data API that simply wraps the
    responses in structured Python objects.
    """

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

    def _url(self, endpoint: str) -> str:
        return "/".join((self._base_url, endpoint))

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
            self, endpoint: str, request: req.DataApiRequest
    ) -> Sequence[Mapping[str, Any]]:
        params = request.dict(by_alias=True)
        response = httpx.get(
            url=self._url(endpoint),
            params=self._update_params(params),
        )
        body = response.json()
        if response.status_code == 403:
            raise InsufficientPermissionsError
        return body["data"]

    def tickers(self, request: req.TickersRequest) -> Sequence[res.TickerResponse]:
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
        data = self._get("tickers", request)
        return [res.TickerResponse(**v) for v in data]

    def strikes(self, request: req.StrikesRequest) -> Sequence[res.StrikeResponse]:
        """Retrieves strikes data for the given asset(s).

        See the corresponding `Strikes`_ endpoint.

        Args:
          request:
            Strikes request object.

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get("strikes", request)
        return [res.StrikeResponse(**v) for v in data]

    def strikes_history(
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
        data = self._get("hist/strikes", request)
        return [res.StrikeResponse(**v) for v in data]

    def strikes_by_options(
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
        data = self._get("strikes/options", request)
        return [res.StrikeResponse(**v) for v in data]

    def strikes_history_by_options(
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
        data = self._get("hist/strikes/options", request)
        return [res.StrikeResponse(**v) for v in data]

    def monies_implied(
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
        data = self._get("monies/implied", request)
        return [res.MoneyImpliedResponse(**v) for v in data]

    def monies_implied_history(
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
        data = self._get("hist/monies/implied", request)
        return [res.MoneyImpliedResponse(**v) for v in data]

    def monies_forecast(
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
        data = self._get("monies/forecast", request)
        return [res.MoneyForecastResponse(**v) for v in data]

    def monies_forecast_history(
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
        data = self._get("hist/monies/forecast", request)
        return [res.MoneyForecastResponse(**v) for v in data]

    def summaries(
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
        data = self._get("summaries", request)
        return [res.SmvSummaryResponse(**v) for v in data]

    def summaries_history(
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
        data = self._get("hist/summaries", request)
        return [res.SmvSummaryResponse(**v) for v in data]

    def core_data(self, request: req.CoreDataRequest) -> Sequence[res.CoreResponse]:
        """Retrieves Core data.

        See the corresponding `Core Data`_ endpoint.

        Args:
          request:
            CoreData request object.

        Returns:
          A list of core data for each specified asset.
        """
        data = self._get("cores", request)
        return [res.CoreResponse(**v) for v in data]

    def core_data_history(
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
        data = self._get("hist/cores", request)
        return [res.CoreResponse(**v) for v in data]

    def daily_price(
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
        data = self._get("hist/dailies", request)
        return [res.DailyPriceResponse(**v) for v in data]

    def historical_volatility(
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
        data = self._get("hist/hvs", request)
        return [res.HistoricalVolatilityResponse(**v) for v in data]

    def dividend_history(
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
        data = self._get("hist/divs", request)
        return [res.DividendHistoryResponse(**v) for v in data]

    def earnings_history(
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
        data = self._get("hist/earnings", request)
        return [res.EarningsHistoryResponse(**v) for v in data]

    def stock_split_history(
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
        data = self._get("hist/splits", request)
        return [res.StockSplitHistoryResponse(**v) for v in data]

    def iv_rank(
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
        data = self._get("ivrank", request)
        return [res.IvRankResponse(**v) for v in data]

    def iv_rank_history(
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
        data = self._get("hist/ivrank", request)
        return [res.IvRankResponse(**v) for v in data]
