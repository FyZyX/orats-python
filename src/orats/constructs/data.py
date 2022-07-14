"""Higher level constructs built on top of base API."""

import datetime
from typing import Iterable, Sequence, Tuple, Collection, Union

from pydantic import BaseModel

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


class Quote(BaseModel):
    price: float
    size: float
    iv: float = None


class Greeks(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    phi: float


class Option(BaseModel):
    underlying: Asset
    expiration: datetime.date
    strike: float
    price: float = None
    spot: float = None
    volume: int = None
    open_interest: int = None
    iv: float = None
    greeks: Greeks = None
    bid: Quote = None
    offer: Quote = None


class CallOption(Option):
    pass


class PutOption(Option):
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
        self._response = endpoint(request)
        return self._response

    def filter_by_days_to_expiration(
        self,
        lower_bound: int = -1,
        upper_bound: int = -1,
    ):
        """Keep only those options within the specified range of days to expiration.

        Args:
          lower_bound:
            Smallest number of days to expiration allowed.
            If not specified, no bound will be set.
          upper_bound:
            Largest number of days to expiration allowed.
            If not specified, no bound will be set.

        Returns:
          A list of strikes for each specified asset.
        """
        self._expiration_range = _bounded_range(lower_bound, upper_bound)

    def filter_by_delta(
        self,
        lower_bound: float = -1,
        upper_bound: float = -1,
    ):
        self._expiration_range = _bounded_range(lower_bound, upper_bound)

    def options(self, trade_date: datetime.date = None):
        # https://blog.orats.com/option-greeks-are-the-same-for-calls-and-puts
        return self._get_strikes(trade_date)

    def calls(self, trade_date: datetime.date = None):
        return [
            CallOption(
                underlying=Asset(strike.underlying_symbol),
                expiration=strike.expiration_date,
                strike=strike.strike,
                price=strike.call_value,
                spot=strike.spot_price,
                volume=strike.call_volume,
                open_interest=strike.call_open_interest,
                iv=strike.iv,
                greeks=Greeks(
                    delta=strike.delta,
                    gamma=strike.gamma,
                    theta=strike.theta,
                    vega=strike.vega,
                    rho=strike.rho,
                    phi=strike.phi,
                ),
                bid=Quote(
                    price=strike.call_bid_price,
                    size=strike.call_bid_size,
                    iv=strike.call_bid_iv,
                ),
                offer=Quote(
                    price=strike.call_ask_price,
                    size=strike.call_ask_size,
                    iv=strike.call_ask_iv,
                ),
            )
            for strike in self._get_strikes(trade_date)
        ]

    def puts(self, trade_date: datetime.date = None):
        return [
            PutOption(
                underlying=Asset(strike.underlying_symbol),
                expiration=strike.expiration_date,
                strike=strike.strike,
                price=strike.put_value,
                spot=strike.spot_price,
                volume=strike.put_volume,
                open_interest=strike.put_open_interest,
                iv=strike.iv,
                greeks=Greeks(
                    delta=strike.delta - 1,
                    gamma=strike.gamma,
                    theta=strike.theta,
                    vega=strike.vega,
                    rho=strike.rho,
                    phi=strike.phi,
                ),
                bid=Quote(
                    price=strike.put_bid_price,
                    size=strike.put_bid_size,
                    iv=strike.put_bid_iv,
                ),
                offer=Quote(
                    price=strike.put_ask_price,
                    size=strike.put_ask_size,
                    iv=strike.put_ask_iv,
                ),
            )
            for strike in self._get_strikes(trade_date)
        ]


class StrikeSearchEndpoint:
    def query(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
        expiration_range: Tuple[int, int] = None,
        delta_range: Tuple[float, float] = None,
    ) -> Sequence[res.StrikeResponse]:
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
        data = self._get(
            "hist/splits",
            ticker=",".join(symbols),
        )
        return [res.StockSplitHistoryResponse(**e) for e in data]
