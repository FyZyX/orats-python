"""Higher level constructs for underlying assets."""

import datetime
from typing import Tuple, Sequence, Set

from pydantic import Field

import orats.endpoints.data as endpoints
from orats.constructs.api.data import request as req
from orats.constructs.api.data import response as res
from orats.constructs.common import IndustryConstruct


class Asset(IndustryConstruct[req.TickersRequest, res.Ticker]):
    """Represents the underlying asset of an option contract."""

    ticker: str = Field(..., description="The ticker symbol of the underlying asset.")

    def _get_ticker(self):
        endpoint = endpoints.TickersEndpoint(self._token)
        request = req.TickersRequest(ticker=self.ticker)
        return self._make_request(endpoint, request)

    def historical_data_range(self) -> Tuple[datetime.date, datetime.date]:
        """The duration of available historical data.

        Returns:
          The minimum and maximum dates of available data.
        """
        ticker = self._get_ticker()
        return ticker.min_date, ticker.max_date


class Universe(IndustryConstruct):
    assets: Set[Asset]


class PriceHistory(IndustryConstruct):
    def _get_daily_prices(self):
        pass


class VolatilityHistory(
    IndustryConstruct[req.HistoricalVolatilityRequest, res.HistoricalVolatility]
):
    tickers: Sequence[str]
    _periods = [5, 10, 20, 30, 60, 90, 100, 120, 252, 500, 1000]

    def _get_historical_volatility(self):
        endpoint = endpoints.HistoricalVolatilityEndpoint(self._token)
        request = req.HistoricalVolatilityRequest(
            tickers=self.tickers,
        )
        return self._make_request(endpoint, request)

    def intraday(self, exclude_earnings: bool = True):
        history = self._get_historical_volatility()
        results = {}
        if not exclude_earnings:
            results[1] = history.hv_1_day
            values = [
                history.hv_5_day,
                history.hv_10_day,
                history.hv_20_day,
                history.hv_30_day,
                history.hv_60_day,
                history.hv_90_day,
                history.hv_100_day,
                history.hv_120_day,
                history.hv_252_day,
                history.hv_500_day,
                history.hv_1000_day,
            ]
        else:
            values = [
                history.hv_ex_earnings_5_day,
                history.hv_ex_earnings_10_day,
                history.hv_ex_earnings_20_day,
                history.hv_ex_earnings_30_day,
                history.hv_ex_earnings_60_day,
                history.hv_ex_earnings_90_day,
                history.hv_ex_earnings_100_day,
                history.hv_ex_earnings_120_day,
                history.hv_ex_earnings_252_day,
                history.hv_ex_earnings_500_day,
                history.hv_ex_earnings_1000_day,
            ]
        results.update(zip(self._periods, values))
        return results

    def close_to_close(self, exclude_earnings: bool = False):
        history = self._get_historical_volatility()
        if not exclude_earnings:
            values = [
                history.close_to_close_hv_5_day,
                history.close_to_close_hv_10_day,
                history.close_to_close_hv_20_day,
                history.close_to_close_hv_30_day,
                history.close_to_close_hv_60_day,
                history.close_to_close_hv_90_day,
                history.close_to_close_hv_100_day,
                history.close_to_close_hv_120_day,
                history.close_to_close_hv_252_day,
                history.close_to_close_hv_500_day,
                history.close_to_close_hv_1000_day,
            ]
        else:
            values = [
                history.close_to_close_hv_ex_earnings_5_day,
                history.close_to_close_hv_ex_earnings_10_day,
                history.close_to_close_hv_ex_earnings_20_day,
                history.close_to_close_hv_ex_earnings_30_day,
                history.close_to_close_hv_ex_earnings_60_day,
                history.close_to_close_hv_ex_earnings_90_day,
                history.close_to_close_hv_ex_earnings_100_day,
                history.close_to_close_hv_ex_earnings_120_day,
                history.close_to_close_hv_ex_earnings_252_day,
                history.close_to_close_hv_ex_earnings_500_day,
                history.close_to_close_hv_ex_earnings_1000_day,
            ]
        return dict(zip(self._periods, values))
