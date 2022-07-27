import datetime
from typing import Sequence

from orats.constructs.api import data as constructs
from orats.endpoints.data import request as req
from orats.sandbox import common
from orats.sandbox.api.generator import FakeDataGenerator


class FakeDataApi:
    """Fake data generator that acts exactly like the actual Data API.

    Use this class when testing out the functionality of this library
    or when developing your own application code. This avoids extraneous
    API calls during the development process.
    """

    def __init__(self):
        self._universe = common.universe()
        self._trade_date = datetime.date.today()
        self._updated = datetime.datetime.now()
        self._generator = FakeDataGenerator()

    def tickers(self, request: req.TickersRequest) -> Sequence[constructs.Ticker]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.ticker(ticker) for ticker in universe]
        return common.as_response(constructs.Ticker, results)

    def strikes(self, request: req.StrikesRequest) -> Sequence[constructs.Strike]:
        universe = request.tickers or self._universe
        results = [self._generator.strike(ticker) for ticker in universe]
        return common.as_response(constructs.Strike, results)

    def strikes_by_options(
        self, *requests: req.StrikesByOptionsRequest
    ) -> Sequence[constructs.Strike]:
        results = [self._generator.strike(request.ticker) for request in requests]
        return common.as_response(constructs.Strike, results)

    def monies_implied(
        self, request: req.MoniesRequest
    ) -> Sequence[constructs.MoneyImplied]:
        universe = request.tickers or self._universe
        results = [self._generator.money_implied(ticker) for ticker in universe]
        return common.as_response(constructs.MoneyImplied, results)

    def monies_forecast(
        self, request: req.MoniesRequest
    ) -> Sequence[constructs.MoneyForecast]:
        universe = request.tickers or self._universe
        results = [self._generator.money_forecast(ticker) for ticker in universe]
        return common.as_response(constructs.MoneyForecast, results)

    def summaries(self, request: req.SummariesRequest) -> Sequence[constructs.Summary]:
        universe = request.tickers or self._universe
        results = [self._generator.summary(ticker) for ticker in universe]
        return common.as_response(constructs.Summary, results)

    def core_data(self, request: req.CoreDataRequest) -> Sequence[constructs.Core]:
        universe = request.tickers or self._universe
        results = [self._generator.core(ticker) for ticker in universe]
        return common.as_response(constructs.Core, results)

    def daily_price(
        self, request: req.DailyPriceRequest
    ) -> Sequence[constructs.DailyPrice]:
        universe = request.tickers or self._universe
        results = [self._generator.daily_price(ticker) for ticker in universe]
        return common.as_response(constructs.DailyPrice, results)

    def historical_volatility(
        self, request: req.HistoricalVolatilityRequest
    ) -> Sequence[constructs.HistoricalVolatility]:
        universe = request.tickers or self._universe
        results = [self._generator.historical_volatility(ticker) for ticker in universe]
        return common.as_response(constructs.HistoricalVolatility, results)

    def dividend_history(
        self, request: req.DividendHistoryRequest
    ) -> Sequence[constructs.DividendHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.dividend_history(ticker) for ticker in universe]
        return common.as_response(constructs.DividendHistory, results)

    def earnings_history(
        self, request: req.EarningsHistoryRequest
    ) -> Sequence[constructs.EarningsHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.earnings_history(ticker) for ticker in universe]
        return common.as_response(constructs.EarningsHistory, results)

    def stock_split_history(
        self, request: req.StockSplitHistoryRequest
    ) -> Sequence[constructs.StockSplitHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.stock_split_history(ticker) for ticker in universe]
        return common.as_response(constructs.StockSplitHistory, results)

    def iv_rank(self, request: req.IvRankRequest) -> Sequence[constructs.IvRank]:
        universe = request.tickers or self._universe
        results = [self._generator.iv_rank(ticker) for ticker in universe]
        return common.as_response(constructs.IvRank, results)
