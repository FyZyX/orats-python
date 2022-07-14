import datetime

import pytest

from orats.endpoints.data import DataApi, DataApiEndpoint
from orats.model.data import request as req
from orats.model.data import response as res
from tests.fixtures import load_fixture


@pytest.fixture(autouse=True)
def data_api(monkeypatch):
    monkeypatch.setattr(DataApiEndpoint, "_get", load_fixture)


class TestDataApi:
    _api = DataApi("demo")

    def test_tickers(self):
        request = req.TickersRequest(ticker="IBM")
        tickers = self._api.tickers(request)
        assert len(tickers) == 1
        ticker = tickers[0]
        assert isinstance(ticker, res.TickerResponse)
        assert isinstance(ticker.underlying_symbol, str)
        assert isinstance(ticker.max_date, datetime.date)
        assert isinstance(ticker.min_date, datetime.date)

    def test_strikes(self):
        request = req.StrikesRequest(
            tickers=("IBM",),
            expiration_range=(30, ...),
            delta_range=(0.30, 0.45),
        )
        strikes = self._api.strikes(request)
        for strike in strikes:
            assert isinstance(strike, res.StrikeResponse)

    def test_strikes_history(self):
        request = req.StrikesHistoryRequest(
            tickers=("IBM", "AAPL"),
            trade_date=datetime.date(2022, 7, 5),
            expiration_range=(30, ...),
            delta_range=(0.30, 0.45),
        )
        strikes = self._api.strikes_history(request)
        for strike in strikes:
            assert isinstance(strike, res.StrikeResponse)

    def test_strikes_by_options(self):
        request = req.StrikesByOptionsRequest(
            ticker="IBM",
            expiration_date=datetime.date(2022, 6, 17),
            strike=50,
        )
        strikes = self._api.strikes_by_options(request)
        for strike in strikes:
            assert isinstance(strike, res.StrikeResponse)

    def test_strikes_history_by_options(self):
        request = req.StrikesHistoryByOptionsRequest(
            ticker="IBM",
            trade_date=datetime.date(2022, 6, 6),
            expiration_date=datetime.date(2022, 6, 17),
            strike=140,
        )
        strikes = self._api.strikes_history_by_options(request)
        for strike in strikes:
            assert isinstance(strike, res.StrikeResponse)

    def test_monies_implied(self):
        request = req.MoniesRequest(
            tickers=("IBM",),
        )
        monies = self._api.monies_implied(request)
        for money in monies:
            assert isinstance(money, res.MoneyImpliedResponse)

    def test_monies_implied_history(self):
        request = req.MoniesHistoryRequest(
            tickers=("IBM",),
            trade_date=datetime.date(2022, 7, 5),
        )
        monies = self._api.monies_implied_history(request)
        for money in monies:
            assert isinstance(money, res.MoneyImpliedResponse)

    def test_monies_forecast(self):
        request = req.MoniesRequest(
            tickers=("IBM",),
        )
        monies = self._api.monies_forecast(request)
        for money in monies:
            assert isinstance(money, res.MoneyForecastResponse)

    def test_monies_forecast_history(self):
        request = req.MoniesHistoryRequest(
            tickers=("IBM",),
            trade_date=datetime.date(2022, 7, 5),
        )
        monies = self._api.monies_forecast_history(request)
        for money in monies:
            assert isinstance(money, res.MoneyForecastResponse)

    def test_summaries(self):
        request = req.SummariesRequest(
            tickers=("IBM",),
        )
        summaries = self._api.summaries(request)
        for summary in summaries:
            assert isinstance(summary, res.SmvSummaryResponse)

    def test_summaries_history(self):
        request = req.SummariesHistoryRequest(
            tickers=("IBM",),
            trade_date=datetime.date(2022, 7, 5),
        )
        summaries = self._api.summaries_history(request)
        for summary in summaries:
            assert isinstance(summary, res.SmvSummaryResponse)

    def test_core_data(self):
        request = req.CoreDataRequest(
            tickers=("IBM",),
        )
        core_data = self._api.core_data(request)
        for core in core_data:
            assert isinstance(core, res.CoreResponse)

    def test_core_data_history(self):
        request = req.CoreDataHistoryRequest(
            tickers=("IBM",),
            trade_date=datetime.date(2022, 7, 5),
        )
        core_data = self._api.core_data_history(request)
        for core in core_data:
            assert isinstance(core, res.CoreResponse)

    def test_daily_price(self):
        request = req.DailyPriceRequest(
            tickers=("IBM",),
        )
        daily_price = self._api.daily_price(request)
        for price in daily_price:
            assert isinstance(price, res.DailyPriceResponse)

    def test_historical_volatility(self):
        request = req.HistoricalVolatilityRequest(
            tickers=("IBM",),
        )
        historical_volatility = self._api.historical_volatility(request)
        for vol in historical_volatility:
            assert isinstance(vol, res.HistoricalVolatilityResponse)

    def test_dividend_history(self):
        request = req.DividendHistoryRequest(ticker="IBM")
        dividend_history = self._api.dividend_history(request)
        for dividend in dividend_history:
            assert isinstance(dividend, res.DividendHistoryResponse)

    def test_earnings_history(self):
        request = req.EarningsHistoryRequest(ticker="IBM")
        earnings_history = self._api.earnings_history(request)
        for earnings in earnings_history:
            assert isinstance(earnings, res.EarningsHistoryResponse)

    def test_stock_split_history(self):
        request = req.StockSplitHistoryRequest(ticker="IBM")
        stock_split_history = self._api.stock_split_history(request)
        for stock_split in stock_split_history:
            assert isinstance(stock_split, res.StockSplitHistoryResponse)

    def test_iv_rank(self):
        request = req.IvRankRequest(
            tickers=("IBM",),
        )
        iv_rank = self._api.iv_rank(request)
        for iv in iv_rank:
            assert isinstance(iv, res.IvRankResponse)

    def test_iv_rank_history(self):
        request = req.IvRankHistoryRequest(
            tickers=("IBM",),
            trade_date=datetime.date(2022, 7, 5),
        )
        iv_rank = self._api.iv_rank_history(request)
        for iv in iv_rank:
            assert isinstance(iv, res.IvRankResponse)
