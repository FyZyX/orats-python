"""
ORATS Data API.

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

import datetime
from typing import Any, Iterable, Mapping, Sequence, Tuple

import httpx

from orats.model.core import Core
from orats.model.money import MoneyForecast, MoneyImplied
from orats.model.strike import Strike
from orats.model.summary import SmvSummary
from orats.model.underlying import (
    Ticker,
    DailyPrice,
    DividendHistory,
    EarningsHistory,
    StockSplitHistory,
)
from orats.model.volatility import HistoricalVolatility, IvRank


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

    def _url(self, path):
        return "/".join((self._base_url, path))

    def _update_params(self, params: Mapping[str, Any]):
        updated_params = dict(token=self._token)
        for key, param in params.items():
            if param is None:
                continue
            updated_params[key] = param
        return updated_params

    def _get(self, path: str, **params: Any):
        response = httpx.get(
            url=self._url(path),
            params=self._update_params(params),
        )
        return response.json()["data"]

    def tickers(self, symbol: str = None) -> Sequence[Ticker]:
        """Retrieves the duration of available data for various assets.

        If no underlying asset is specified, the result will be a list
        of all available ticker symbols. Each symbol is accompanied by
        a start (min) and end (max) date for which data is available.
        See the corresponding `Tickers`_ endpoint.

        Args:
          symbol:
            The ticker symbol of the underlying asset.

        Returns:
          A list of tickers with data durations.
        """
        data = self._get("tickers", ticker=symbol)
        return [Ticker(**t) for t in data]

    def strikes(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
        days_to_expiration: Tuple[int, int] = None,
        delta: Tuple[float, float] = None,
    ) -> Sequence[Strike]:
        """Retrieves strikes data for the given asset(s).

        See the corresponding `Strikes`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          fields:
            The subset of fields to retrieve.
          days_to_expiration:
            Filters results to a range of days to expiration.
            Specified as a (min, max) range of integers.
            Example: (30, 45)
          delta:
            Filters results to a range of delta values.
            Specified as a (min, max) range of floating point numbers.
            Example: (.30, .45)

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get(
            "strikes",
            ticker=",".join(symbols),
            fields=",".join(fields) if fields else fields,
            dte=",".join([str(d) for d in days_to_expiration])
            if days_to_expiration
            else days_to_expiration,
            delta=",".join([str(d) for d in delta]) if delta else delta,
        )
        return [Strike(**s) for s in data]

    def strikes_history(
        self,
        *symbols: str,
        trade_date: datetime.date,
        fields: Iterable[str] = None,
        days_to_expiration: Tuple[int, int] = None,
        delta: Tuple[float, float] = None,
    ) -> Sequence[Strike]:
        """Retrieves end of day strikes data for the given asset(s).

        See the corresponding `Strikes History`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.
          days_to_expiration:
            Filters results to a range of days to expiration.
            Specified as a (min, max) range of integers.
            Example: (30, 45)
          delta:
            Filters results to a range of delta values.
            Specified as a (min, max) range of floating point numbers.
            Example: (.30, .45)

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get(
            "hist/strikes",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=",".join(fields) if fields else fields,
            dte=",".join([str(d) for d in days_to_expiration])
            if days_to_expiration
            else days_to_expiration,
            delta=",".join([str(d) for d in delta]) if delta else delta,
        )
        return [Strike(**s) for s in data]

    def strikes_by_options(
        self,
        symbol: str,
        expiration_date: datetime.date,
        strike: float,
    ) -> Sequence[Strike]:
        """Retrieves current strikes data by ticker, expiry, and strike.

        See the corresponding `Strikes by Options`_ endpoint.

        Args:
          symbol:
            The ticker symbol of the underlying asset.
          expiration_date:
            The expiration date to retrieve.
          strike:
            The strike price to retrieve.

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get(
            "strikes/options",
            ticker=symbol,
            expirDate=expiration_date,
            strike=strike,
        )
        return [Strike(**s) for s in data]

    def strikes_history_by_options(
        self,
        symbol: str,
        expiration_date: datetime.date,
        strike: float,
        trade_date: datetime.date = None,
    ) -> Sequence[Strike]:
        """Retrieves current strikes data by ticker, expiry, and strike.

        See the corresponding `Strikes History by Options`_ endpoint.

        Args:
          symbol:
            The ticker symbol of the underlying asset.
          trade_date:
            The trade date to retrieve.
          expiration_date:
            The expiration date to retrieve.
          strike:
            The strike price to retrieve.

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get(
            "hist/strikes/options",
            ticker=symbol,
            tradeDate=trade_date,
            expirDate=expiration_date,
            strike=strike,
        )
        return [Strike(**s) for s in data]

    def monies_implied(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyImplied]:
        """Retrieves monthly implied data for monies.

        See the corresponding `Monies`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of implied monies for each specified asset.
        """
        data = self._get(
            "monies/implied",
            ticker=",".join(symbols),
            fields=",".join(fields) if fields else fields,
        )
        return [MoneyImplied(**m) for m in data]

    def monies_forecast(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyForecast]:
        """Retrieves monthly forecast data for monies.

        See the corresponding `Monies`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of forecast monies for each specified asset.
        """
        data = self._get(
            "monies/forecast",
            ticker=",".join(symbols),
            fields=",".join(fields) if fields else fields,
        )
        return [MoneyForecast(**m) for m in data]

    def monies_implied_history(
        self,
        *symbols: str,
        trade_date: datetime.date,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyImplied]:
        """Retrieves end of day monthly implied history data for monies.

        See the corresponding `Monies History`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of implied monies for each specified asset.
        """
        data = self._get(
            "hist/monies/implied",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=",".join(fields) if fields else fields,
        )
        return [MoneyImplied(**m) for m in data]

    def monies_forecast_history(
        self,
        *symbols: str,
        trade_date: datetime.date,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyForecast]:
        """Retrieves monthly forecast history data for monies.

        See the corresponding `Monies History`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of forecast monies for each specified asset.
        """
        data = self._get(
            "hist/monies/forecast",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=",".join(fields) if fields else fields,
        )
        return [MoneyForecast(**m) for m in data]

    def summaries(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[SmvSummary]:
        """Retrieves SMV Summary data.

        See the corresponding `Summaries`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of SMV summaries for each specified asset.
        """
        data = self._get(
            "summaries",
            ticker=",".join(symbols),
            fields=",".join(fields) if fields else fields,
        )
        return [SmvSummary(**s) for s in data]

    def summaries_history(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[SmvSummary]:
        """Retrieves SMV Summary data.

        See the corresponding `Summaries History`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of SMV summaries for each specified asset.
        """
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/summaries",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=",".join(fields) if fields else fields,
        )
        return [SmvSummary(**m) for m in data]

    def core_data(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[Core]:
        """Retrieves Core data.

        See the corresponding `Core Data`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of core data for each specified asset.
        """
        data = self._get(
            "cores",
            ticker=",".join(symbols),
            fields=",".join(fields) if fields else fields,
        )
        return [Core(**c) for c in data]

    def core_data_history(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[Core]:
        """Retrieves end of day Core history data.

        See the corresponding `Core Data History`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of core data for each specified asset.
        """
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/cores",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=",".join(fields) if fields else fields,
        )
        return [Core(**c) for c in data]

    def daily_price(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[DailyPrice]:
        """Retrieves end of day daily stock price data.

        See the corresponding `Daily Price`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of daily price data for each specified asset.
        """
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/dailies",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=",".join(fields) if fields else fields,
        )
        return [DailyPrice(**p) for p in data]

    def historical_volatility(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[HistoricalVolatility]:
        """Retrieves historical volatility data.

        See the corresponding `Historical Volatility`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of historical volatility data for each specified asset.
        """
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/hvs",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=",".join(fields) if fields else fields,
        )
        return [HistoricalVolatility(**hv) for hv in data]

    def dividend_history(
        self,
        *symbols: str,
    ) -> Sequence[DividendHistory]:
        data = self._get(
            "hist/divs",
            ticker=",".join(symbols),
        )
        return [DividendHistory(**d) for d in data]

    def earnings_history(
        self,
        *symbols: str,
    ) -> Sequence[EarningsHistory]:
        data = self._get(
            "hist/earnings",
            ticker=",".join(symbols),
        )
        return [EarningsHistory(**e) for e in data]

    def stock_split_history(
        self,
        *symbols: str,
    ) -> Sequence[StockSplitHistory]:
        data = self._get(
            "hist/splits",
            ticker=",".join(symbols),
        )
        return [StockSplitHistory(**e) for e in data]

    def iv_rank(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[IvRank]:
        data = self._get(
            "ivrank",
            ticker=",".join(symbols),
            fields=fields,
        )
        return [IvRank(**e) for e in data]

    def iv_rank_history(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[IvRank]:
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/ivrank",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
        return [IvRank(**e) for e in data]
