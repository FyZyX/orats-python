"""Higher level constructs built on top of base API."""

import datetime
from typing import Iterable, Sequence, Tuple, Collection, Union

import orats.endpoints.data as endpoints
from orats.model.data import request as req
from orats.model.data import response as res


def _bounded_range(lower_bound, upper_bound):
    if lower_bound < 0 and upper_bound < 0:
        return None
    elif lower_bound < 0:
        l, u = ..., upper_bound
    elif upper_bound < 0:
        l, u = lower_bound, ...
    else:
        l, u = lower_bound, upper_bound
    return req.BoundedRange(l, u)


class Asset:
    """Represents the underlying asset of an option contract."""

    def __init__(self, ticker: str, token: str = None):
        """Initializes an asset object.

        Args:
          ticker:
            The ticker symbol of the underlying asset.
          token:
            API token.
        """
        self._ticker = ticker
        self._token = token
        self._response = None

    def _get_ticker(self):
        if self._response:
            return self._response
        endpoint = endpoints.TickersEndpoint(self._token)
        request = req.TickersRequest(ticker=self._ticker)
        # TODO: Error handling
        self._response = endpoint(request)[0]
        return self._response

    def historical_data_range(self) -> (datetime.date, datetime.date):
        """The duration of available historical data.

        Returns:
          The minimum and maximum dates of available data.
        """
        ticker = self._get_ticker()
        return ticker.min_date, ticker.max_date


class Universe:
    def __init__(self, tickers: Collection):
        self._assets: Collection[Asset] = {Asset(ticker) for ticker in tickers}


class Option:
    pass


class CallOption:
    pass


class PutOption:
    pass


class OptionChain:
    def __init__(self, ticker: str, token: str = None):
        """Initializes an asset object.

        Args:
          ticker:
            The ticker symbol of the underlying asset.
          token:
            API token.
        """
        self._ticker = ticker
        self._token = token
        self._expiration_range = None
        self._delta_range = None
        self._response = None

    def _get_strikes(self, trade_date: datetime.date = None):
        if self._response:
            return self._response

        if trade_date:
            endpoint = endpoints.StrikesHistoryEndpoint(self._token)
            request = req.StrikesHistoryRequest(
                tickers=self._ticker,
                trade_date=trade_date,
                expiration_range=self._expiration_range,
                delta_range=self._delta_range,
            )
        else:
            endpoint = endpoints.StrikesEndpoint(self._token)
            request = req.StrikesRequest(
                tickers=self._ticker,
                expiration_range=self._expiration_range,
                delta_range=self._delta_range,
            )

        # TODO: Error handling
        self._response = endpoint(request)[0]
        return self._response

    def filter_by_days_to_expiration(
        self,
        lower_bound: int = -1,
        upper_bound: int = -1,
    ):
        self._expiration_range = _bounded_range(lower_bound, upper_bound)

    def filter_by_delta(
        self,
        lower_bound: float = -1,
        upper_bound: float = -1,
    ):
        self._expiration_range = _bounded_range(lower_bound, upper_bound)

    def table(self, trade_date: datetime.date = None):
        return self._get_strikes(trade_date)


class StrikeSearchEndpoint:
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
        expiration_range: Tuple[int, int] = None,
        delta_range: Tuple[float, float] = None,
    ) -> Sequence[res.StrikeResponse]:
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
        return [res.StrikeResponse(**s) for s in data]


class StrikeEndpoint:
    def query(
        self,
        symbol: str,
        expiration_date: datetime.date,
        strike: float,
        trade_date: datetime.date = None,
    ) -> Sequence[res.StrikeResponse]:
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
        return [res.StrikeResponse(**s) for s in data]


class MoniesImpliedEndpoint:
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[res.MoneyImpliedResponse]:
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
        return [res.MoneyImpliedResponse(**m) for m in data]


class MoniesForecastEndpoint:
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[res.MoneyForecastResponse]:
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
        return [res.MoneyForecastResponse(**m) for m in data]


class SummariesEndpoint:
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[res.SmvSummaryResponse]:
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
        return [res.SmvSummaryResponse(**m) for m in data]


class CoreDataEndpoint:
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[res.CoreResponse]:
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
        return [res.CoreResponse(**c) for c in data]


class IvRankEndpoint:
    def iv_rank(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[res.IvRankResponse]:
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
        return [res.IvRankResponse(**e) for e in data]


class HistoricalVolatilityEndpoint:
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[res.HistoricalVolatilityResponse]:
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
        return [res.HistoricalVolatilityResponse(**hv) for hv in data]


class DailyPriceEndpoint:
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[res.DailyPriceResponse]:
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
        return [res.DailyPriceResponse(**p) for p in data]


class DividendHistoryEndpoint:
    def query(
        self,
        *symbols: str,
    ) -> Sequence[res.DividendHistoryResponse]:
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
        return [res.DividendHistoryResponse(**d) for d in data]


class EarningsHistoryEndpoint:
    def query(
        self,
        *symbols: str,
    ) -> Sequence[res.EarningsHistoryResponse]:
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
        return [res.EarningsHistoryResponse(**e) for e in data]


class StockSplitHistoryEndpoint:
    def query(
        self,
        *symbols: str,
    ) -> Sequence[res.StockSplitHistoryResponse]:
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
        return [res.StockSplitHistoryResponse(**e) for e in data]