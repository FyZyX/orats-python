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

import datetime
from typing import Any, Iterable, Mapping, Sequence, Tuple

import httpx

from orats.errors import InsufficientPermissionsError
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

    def _url(self, path: str, historical: bool = False):
        return "/".join((self._base_url, f"hist/{path}" if historical else path))

    def _update_params(self, params: Mapping[str, Any]):
        updated_params = dict(token=self._token)
        for key, param in params.items():
            if param is None:
                continue
            updated_params[key] = param
        return updated_params

    def _get(
        self,
        path: str,
        fields: Iterable[str] = None,
        trade_date: datetime.date = None,
        **params: Any,
    ):
        if trade_date is not None:
            params.update(
                tradeDate=trade_date,
            )
        if fields is not None:
            params.update(
                fields=",".join(fields),
            )
        response = httpx.get(
            url=self._url(path, historical=trade_date is not None),
            params=self._update_params(params),
        )
        body = response.json()
        if response.status_code == 403:
            raise InsufficientPermissionsError
        for x in body["data"]:
            print(x["dte"])
        return body["data"]


class TickersEndpoint(DataApiEndpoint):
    def query(self, symbol: str = None) -> Sequence[Ticker]:
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


class StrikeSearchEndpoint(DataApiEndpoint):
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
        expiration_range: Tuple[int, int] = None,
        delta_range: Tuple[float, float] = None,
    ) -> Sequence[Strike]:
        """Retrieves strikes data for the given asset(s).

        Specify a trade date to retrieve historical end of day values.
        See the corresponding `Strikes`_ and `Strikes History`_ endpoints.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.
          expiration_range:
            Filters results to a range of days to expiration.
            Specified as a ``(min, max)`` range of integers.
            To ignore an upper/lower bound, use `...` as a placeholder.
            Examples: ``(30, 45)``, ``(30, ...)``, ``(..., 45)``
          delta_range:
            Filters results to a range of delta values.
            Specified as a ``(min, max)`` range of floating point numbers.
            To ignore an upper/lower bound, use ``...`` as a placeholder.
            Examples: ``(.30, .45)``, ``(.30, ...)``, ``(..., .45)``

        Returns:
          A list of strikes for each specified asset.
        """
        data = self._get(
            "strikes",
            ticker=",".join(symbols),
            trade_date=trade_date,
            fields=fields,
            dte=",".join([str(d) for d in expiration_range])
            if expiration_range
            else expiration_range,
            delta=",".join([str(d) for d in delta_range])
            if delta_range
            else delta_range,
        )
        return [Strike(**s) for s in data]


class StrikeEndpoint(DataApiEndpoint):
    def query(
        self,
        symbol: str,
        expiration_date: datetime.date,
        strike: float,
        trade_date: datetime.date = None,
    ) -> Sequence[Strike]:
        """Retrieves strikes data by ticker, expiry, and strike.

        Specify a trade date to retrieve historical end of day values.
        See the corresponding `Strikes by Options`_ and
        `Strikes History by Options`_ endpoints.

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
            "strikes/options",
            ticker=symbol,
            trade_date=trade_date,
            expirDate=expiration_date,
            strike=strike,
        )
        return [Strike(**s) for s in data]


class MoniesImpliedEndpoint(DataApiEndpoint):
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyImplied]:
        """Retrieves end of day monthly implied history data for monies.

        Specify a trade date to retrieve historical end of day values.
        See the corresponding `Monies`_ and `Monies History`_ endpoints.

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
            "monies/implied",
            ticker=",".join(symbols),
            trade_date=trade_date,
            fields=fields,
        )
        return [MoneyImplied(**m) for m in data]


class MoniesForecastEndpoint(DataApiEndpoint):
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyForecast]:
        """Retrieves monthly forecast history data for monies.

        Specify a trade date to retrieve historical end of day values.
        See the corresponding `Monies`_ and `Monies History`_ endpoints.

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
            "monies/forecast",
            ticker=",".join(symbols),
            trade_date=trade_date,
            fields=fields,
        )
        return [MoneyForecast(**m) for m in data]


class SummariesEndpoint(DataApiEndpoint):
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[SmvSummary]:
        """Retrieves SMV Summary data.

        Specify a trade date to retrieve historical end of day values.
        See the corresponding `Summaries`_ and `Summaries History`_ endpoints.

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
            "summaries",
            ticker=",".join(symbols),
            trade_date=trade_date,
            fields=fields,
        )
        return [SmvSummary(**m) for m in data]


class CoreDataEndpoint(DataApiEndpoint):
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[Core]:
        """Retrieves Core history data.

        Specify a trade date to retrieve historical end of day values.
        See the corresponding `Core Data`_ and `Core Data History`_ endpoints.

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
            "cores",
            ticker=",".join(symbols),
            trade_date=trade_date,
            fields=fields,
        )
        return [Core(**c) for c in data]


class IvRankEndpoint(DataApiEndpoint):
    def iv_rank(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[IvRank]:
        """Retrieves IV rank data.

        Specify a trade date to retrieve historical end of day values.
        See the corresponding `IV Rank`_ and `IV Rank History`_ endpoints.

        Args:
          symbols:
            List of assets to retrieve.
          trade_date:
            The trade date to retrieve.
          fields:
            The subset of fields to retrieve.

        Returns:
          A list of IV rank history data for each specified asset.
        """
        assert len(symbols) and trade_date is not None
        data = self._get(
            "ivrank",
            ticker=",".join(symbols),
            trade_date=trade_date,
            fields=fields,
        )
        return [IvRank(**e) for e in data]


class HistoricalVolatilityEndpoint(DataApiEndpoint):
    def query(
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
            "hvs",
            ticker=",".join(symbols),
            trade_date=trade_date,
            fields=fields,
        )
        return [HistoricalVolatility(**hv) for hv in data]


class DailyPriceEndpoint(DataApiEndpoint):
    def query(
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
            "dailies",
            ticker=",".join(symbols),
            trade_date=trade_date,
            fields=fields,
        )
        return [DailyPrice(**p) for p in data]


class DividendHistoryEndpoint(DataApiEndpoint):
    def query(
        self,
        *symbols: str,
    ) -> Sequence[DividendHistory]:
        """Retrieves dividend history data.

        See the corresponding `Dividend History`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.

        Returns:
          A list of dividend history data for each specified asset.
        """
        data = self._get(
            "hist/divs",
            ticker=",".join(symbols),
        )
        return [DividendHistory(**d) for d in data]


class EarningsHistoryEndpoint(DataApiEndpoint):
    def query(
        self,
        *symbols: str,
    ) -> Sequence[EarningsHistory]:
        """Retrieves earnings history data.

        See the corresponding `Earnings History`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.

        Returns:
          A list of earnings history data for each specified asset.
        """
        data = self._get(
            "hist/earnings",
            ticker=",".join(symbols),
        )
        return [EarningsHistory(**e) for e in data]


class StockSplitHistoryEndpoint(DataApiEndpoint):
    def query(
        self,
        *symbols: str,
    ) -> Sequence[StockSplitHistory]:
        """Retrieves stock split history data.

        See the corresponding `Stock Split History`_ endpoint.

        Args:
          symbols:
            List of assets to retrieve.

        Returns:
          A list of stock split history data for each specified asset.
        """
        data = self._get(
            "hist/splits",
            ticker=",".join(symbols),
        )
        return [StockSplitHistory(**e) for e in data]


class DataApi:
    """Low-level interface to the `Data API`_.

    A direct translation of the Data API that simply wraps the
    responses in structured Python objects.
    """
