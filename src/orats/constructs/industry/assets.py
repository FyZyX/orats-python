"""Higher level constructs for underlying assets."""

import datetime
from typing import Tuple, Sequence, Set

from orats.constructs.api import data as api_constructs
from orats.constructs.common import IndustryConstruct
from orats.endpoints.data import endpoints, request as req


class AssetAnalyzer:
    def __init__(self, token: str = None, mock: bool = False):
        self._token = token
        self._mock = mock

    def asset(self, ticker: str):
        endpoint = endpoints.TickersEndpoint(self._token, mock=self._mock)
        request = req.TickersRequest(ticker=ticker)
        response = endpoint(request)
        return Asset(ticker=response[0])

    def universe(self):
        endpoint = endpoints.TickersEndpoint(self._token, mock=self._mock)
        request = req.TickersRequest()
        response = endpoint(request)
        return [Asset(ticker=ticker) for ticker in response]

    def price_history(
        self,
        tickers: Sequence[str] = None,
        trade_date: datetime.date = None,
    ):
        endpoint = endpoints.DailyPriceEndpoint(self._token, mock=self._mock)
        request = req.DailyPriceRequest(tickers=tickers, trade_date=trade_date)
        response = endpoint(request)
        return [PriceHistory(history=history) for history in response]

    def historical_volatility(
        self,
        tickers: Sequence[str] = None,
        trade_date: datetime.date = None,
    ):
        endpoint = endpoints.HistoricalVolatilityEndpoint(self._token, mock=self._mock)
        request = req.HistoricalVolatilityRequest(
            tickers=tickers, trade_date=trade_date
        )
        response = endpoint(request)
        return [VolatilityHistory(history=history) for history in response]


class Asset(IndustryConstruct):
    """Represents the underlying asset of an option contract."""

    ticker: api_constructs.Ticker

    def historical_data_range(self) -> Tuple[datetime.date, datetime.date]:
        """The duration of available historical data.

        Returns:
          The minimum and maximum dates of available data.
        """
        return self.ticker.min_date, self.ticker.max_date


class Universe(IndustryConstruct):
    assets: Set[Asset]

    def __iter__(self):
        yield from self.assets

    def symbols(self):
        yield from (asset.ticker for asset in self.assets)


class PriceBar(IndustryConstruct):
    open: float
    high: float
    low: float
    close: float
    volume: int


class PriceHistory(IndustryConstruct):
    history: api_constructs.DailyPrice

    def candle(self):
        return PriceBar(
            open=self.history.unadjusted_open,
            high=self.history.unadjusted_high,
            low=self.history.unadjusted_low,
            close=self.history.unadjusted_close,
            volume=self.history.unadjusted_volume,
        )

    def adjusted_candle(self):
        return PriceBar(
            open=self.history.open,
            high=self.history.high,
            low=self.history.low,
            close=self.history.close,
            volume=self.history.volume,
        )


class VolatilityHistory(IndustryConstruct):
    history: api_constructs.HistoricalVolatility
    _periods = [5, 10, 20, 30, 60, 90, 100, 120, 252, 500, 1000]

    def intraday(self, exclude_earnings: bool = True):
        results = {}
        if not exclude_earnings:
            results[1] = self.history.hv_1_day
            values = [
                self.history.hv_5_day,
                self.history.hv_10_day,
                self.history.hv_20_day,
                self.history.hv_30_day,
                self.history.hv_60_day,
                self.history.hv_90_day,
                self.history.hv_100_day,
                self.history.hv_120_day,
                self.history.hv_252_day,
                self.history.hv_500_day,
                self.history.hv_1000_day,
            ]
        else:
            values = [
                self.history.hv_ex_earnings_5_day,
                self.history.hv_ex_earnings_10_day,
                self.history.hv_ex_earnings_20_day,
                self.history.hv_ex_earnings_30_day,
                self.history.hv_ex_earnings_60_day,
                self.history.hv_ex_earnings_90_day,
                self.history.hv_ex_earnings_100_day,
                self.history.hv_ex_earnings_120_day,
                self.history.hv_ex_earnings_252_day,
                self.history.hv_ex_earnings_500_day,
                self.history.hv_ex_earnings_1000_day,
            ]
        results.update(zip(self._periods, values))
        return results

    def close_to_close(self, exclude_earnings: bool = False):
        if not exclude_earnings:
            values = [
                self.history.close_to_close_hv_5_day,
                self.history.close_to_close_hv_10_day,
                self.history.close_to_close_hv_20_day,
                self.history.close_to_close_hv_30_day,
                self.history.close_to_close_hv_60_day,
                self.history.close_to_close_hv_90_day,
                self.history.close_to_close_hv_100_day,
                self.history.close_to_close_hv_120_day,
                self.history.close_to_close_hv_252_day,
                self.history.close_to_close_hv_500_day,
                self.history.close_to_close_hv_1000_day,
            ]
        else:
            values = [
                self.history.close_to_close_hv_ex_earnings_5_day,
                self.history.close_to_close_hv_ex_earnings_10_day,
                self.history.close_to_close_hv_ex_earnings_20_day,
                self.history.close_to_close_hv_ex_earnings_30_day,
                self.history.close_to_close_hv_ex_earnings_60_day,
                self.history.close_to_close_hv_ex_earnings_90_day,
                self.history.close_to_close_hv_ex_earnings_100_day,
                self.history.close_to_close_hv_ex_earnings_120_day,
                self.history.close_to_close_hv_ex_earnings_252_day,
                self.history.close_to_close_hv_ex_earnings_500_day,
                self.history.close_to_close_hv_ex_earnings_1000_day,
            ]
        return dict(zip(self._periods, values))
