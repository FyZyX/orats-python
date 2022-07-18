"""Higher level constructs for underlying assets."""

import datetime
from typing import Tuple, Collection, Optional, Sequence

from pydantic import BaseModel, Field

import orats.endpoints.data as endpoints
from orats.constructs.api.data import request as req
from orats.constructs.api.data import response as res
from orats.constructs.industry.common import _get_token


class Asset(BaseModel):
    """Represents the underlying asset of an option contract."""

    ticker: str = Field(..., description="The ticker symbol of the underlying asset.")
    token: str = Field(_get_token(), description="API token.")
    _response: Optional[res.Ticker] = None

    def _get_ticker(self):
        if self._response:
            return self._response
        endpoint = endpoints.TickersEndpoint(self.token)
        request = req.TickersRequest(ticker=self.ticker)
        self._response = endpoint(request)[0]
        return self._response

    def historical_data_range(self) -> Tuple[datetime.date, datetime.date]:
        """The duration of available historical data.

        Returns:
          The minimum and maximum dates of available data.
        """
        ticker = self._get_ticker()
        return ticker.min_date, ticker.max_date


class Universe:
    def __init__(self, tickers: Collection):
        self._assets: Collection[Asset] = {Asset(ticker=ticker) for ticker in tickers}


class PriceHistory:
    def _get_daily_prices(self):
        pass


class VolatilityHistory:
    _periods = [5, 10, 20, 30, 60, 90, 100, 120, 252, 500, 1000]
    _periods = [datetime.timedelta(days=n) for n in _periods]

    def __init__(self, tickers: Sequence[str], token: str = None):
        self._tickers = tickers
        self._token = token or _get_token()
        self._response: Optional[res.HistoricalVolatility] = None

    def _get_historical_volatility(self):
        if self._response:
            return self._response
        endpoint = endpoints.HistoricalVolatilityEndpoint(self._token)
        request = req.HistoricalVolatilityRequest(
            tickers=self._tickers,
        )
        self._response = endpoint(request)[0]
        return self._response

    def intraday(self, exclude_earnings: bool = True):
        results = {}
        if not exclude_earnings:
            results[datetime.timedelta(days=1)] = self._response.hv_1_day
            values = [
                self._response.hv_5_day,
                self._response.hv_10_day,
                self._response.hv_20_day,
                self._response.hv_30_day,
                self._response.hv_60_day,
                self._response.hv_90_day,
                self._response.hv_100_day,
                self._response.hv_120_day,
                self._response.hv_252_day,
                self._response.hv_500_day,
                self._response.hv_1000_day,
            ]
        else:
            values = [
                self._response.hv_ex_earnings_5_day,
                self._response.hv_ex_earnings_10_day,
                self._response.hv_ex_earnings_20_day,
                self._response.hv_ex_earnings_30_day,
                self._response.hv_ex_earnings_60_day,
                self._response.hv_ex_earnings_90_day,
                self._response.hv_ex_earnings_100_day,
                self._response.hv_ex_earnings_120_day,
                self._response.hv_ex_earnings_252_day,
                self._response.hv_ex_earnings_500_day,
                self._response.hv_ex_earnings_1000_day,
            ]
        results.update(zip(self._periods, values))
        return results

    def close_to_close(self, exclude_earnings: bool = False):
        if not exclude_earnings:
            values = [
                self._response.close_to_close_hv_5_day,
                self._response.close_to_close_hv_10_day,
                self._response.close_to_close_hv_20_day,
                self._response.close_to_close_hv_30_day,
                self._response.close_to_close_hv_60_day,
                self._response.close_to_close_hv_90_day,
                self._response.close_to_close_hv_100_day,
                self._response.close_to_close_hv_120_day,
                self._response.close_to_close_hv_252_day,
                self._response.close_to_close_hv_500_day,
                self._response.close_to_close_hv_1000_day,
            ]
        else:
            values = [
                self._response.close_to_close_hv_ex_earnings_5_day,
                self._response.close_to_close_hv_ex_earnings_10_day,
                self._response.close_to_close_hv_ex_earnings_20_day,
                self._response.close_to_close_hv_ex_earnings_30_day,
                self._response.close_to_close_hv_ex_earnings_60_day,
                self._response.close_to_close_hv_ex_earnings_90_day,
                self._response.close_to_close_hv_ex_earnings_100_day,
                self._response.close_to_close_hv_ex_earnings_120_day,
                self._response.close_to_close_hv_ex_earnings_252_day,
                self._response.close_to_close_hv_ex_earnings_500_day,
                self._response.close_to_close_hv_ex_earnings_1000_day,
            ]
        return dict(zip(self._periods, values))
