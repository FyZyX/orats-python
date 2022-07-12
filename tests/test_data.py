import datetime
import json
import os.path
import unittest
from unittest import skip

from orats.endpoints.data import DataApi
from orats.model.data import request as req
from orats.model.data import response as res


def test():
    path = os.path.join(os.path.dirname(__file__), "fixtures", "strike.json")
    with open(path) as handle:
        strike = res.StrikeResponse(**json.load(handle))
    print(strike)


class MyDataApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._api = DataApi("demo")

    def test_tickers(self):
        request = req.TickersRequest(ticker="IBM")
        tickers = self._api.tickers(request)
        self.assertEqual(len(tickers), 1)
        ticker = tickers[0]
        self.assertIsInstance(ticker, res.TickerResponse)
        self.assertIsInstance(ticker.underlying_symbol, str)
        self.assertIsInstance(ticker.max_date, datetime.date)
        self.assertIsInstance(ticker.min_date, datetime.date)

    def test_strikes(self):
        request = req.StrikesRequest(
            tickers=("IBM",),
            expiration_range=(30, ...),
            delta_range=(0.30, 0.45),
        )
        strikes = self._api.strikes(request)
        for strike in strikes:
            self.assertIsInstance(strike, res.StrikeResponse)

    @skip
    def test_strikes_history(self):
        request = req.StrikesHistoryRequest(
            tickers=("IBM", "AAPL"),
            trade_date=datetime.date(2022, 7, 5),
            expiration_range=(30, ...),
            delta_range=(0.30, 0.45),
        )
        strikes = self._api.strikes_history(request)
        for strike in strikes:
            self.assertIsInstance(strike, res.StrikeResponse)

    def test_strikes_by_options(self):
        request = req.StrikesByOptionsRequest(
            ticker="IBM",
            expiration_date=datetime.date(2022, 6, 17),
            strike=50,
        )
        strikes = self._api.strikes_by_options(request)
        for strike in strikes:
            self.assertIsInstance(strike, res.StrikeResponse)

    def test_monies_implied(self):
        request = req.MoniesRequest(
            tickers=("IBM",),
        )
        monies = self._api.monies_implied(request)
        for money in monies:
            self.assertIsInstance(money, res.MoneyImpliedResponse)

    def test_monies_forecast(self):
        request = req.MoniesRequest(
            tickers=("IBM",),
        )
        monies = self._api.monies_forecast(request)
        for money in monies:
            self.assertIsInstance(money, res.MoneyForecastResponse)

    def test_summaries(self):
        request = req.SummariesRequest(
            tickers=("IBM",),
        )
        summaries = self._api.summaries(request)
        for summary in summaries:
            self.assertIsInstance(summary, res.SmvSummaryResponse)

    def test_core_date(self):
        request = req.CoreDataRequest(
            tickers=("IBM",),
        )
        core_data = self._api.core_date(request)
        for core in core_data:
            self.assertIsInstance(core, res.CoreResponse)

    def test_daily_price(self):
        request = req.DailyPriceRequest(
            tickers=("IBM",),
        )
        daily_price = self._api.daily_price(request)
        for price in daily_price:
            self.assertIsInstance(price, res.DailyPriceResponse)

    def test_historical_volatility(self):
        request = req.HistoricalVolatilityRequest(
            tickers=("IBM",),
        )
        historical_volatility = self._api.historical_volatility(request)
        for vol in historical_volatility:
            self.assertIsInstance(vol, res.HistoricalVolatilityResponse)

    def test_dividend_history(self):
        request = req.DividendHistoryRequest(ticker="IBM")
        dividend_history = self._api.dividend_history(request)
        for dividend in dividend_history:
            self.assertIsInstance(dividend, res.DividendHistoryResponse)

    def test_earnings_history(self):
        request = req.EarningsHistoryRequest(ticker="IBM")
        earnings_history = self._api.earnings_history(request)
        for earnings in earnings_history:
            self.assertIsInstance(earnings, res.EarningsHistoryResponse)

    def test_stock_split_history(self):
        request = req.StockSplitHistoryRequest(ticker="IBM")
        stock_split_history = self._api.stock_split_history(request)
        for stock_split in stock_split_history:
            self.assertIsInstance(stock_split, res.StockSplitHistoryResponse)

    def test_iv_rank(self):
        request = req.IvRankRequest(
            tickers=("IBM",),
        )
        iv_rank = self._api.iv_rank(request)
        for iv in iv_rank:
            self.assertIsInstance(iv, res.IvRankResponse)


if __name__ == "__main__":
    unittest.main()
