import datetime
from typing import Sequence, Callable, Union

from orats.constructs.api import data as api_constructs
from orats.endpoints.data import request as req
from orats.sandbox import common
from orats.sandbox.api.generator import FakeDataGenerator


class FakeDataApi:
    """Fake data generator that acts exactly like the actual Data API.

    Use this class when testing out the functionality of this library
    or when developing your own application code. This avoids extraneous
    API calls during the development process.
    """

    def __init__(
        self,
        universe=common.universe(),
        trade_date=datetime.date.today(),
        updated=datetime.datetime.now(),
    ):
        self._universe = universe
        self._trade_date = trade_date
        self._updated = updated
        self._generator = FakeDataGenerator()

    def tickers(self, request: req.TickersRequest) -> Sequence[api_constructs.Ticker]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.ticker(ticker) for ticker in universe]
        return common.as_response(api_constructs.Ticker, results)

    def strikes(self, request: req.StrikesRequest) -> Sequence[api_constructs.Strike]:
        universe = request.tickers or self._universe
        results = [self._generator.strike(ticker) for ticker in universe]
        return common.as_response(api_constructs.Strike, results)

    def strikes_by_options(
        self, *requests: req.StrikesByOptionsRequest
    ) -> Sequence[api_constructs.Strike]:
        results = [self._generator.strike(request.ticker) for request in requests]
        return common.as_response(api_constructs.Strike, results)

    def _monies(
        self, request: req.MoniesRequest, func: Callable
    ) -> Sequence[Union[api_constructs.MoneyImplied, api_constructs.MoneyForecast]]:
        universe = request.tickers or self._universe
        monies = []
        for ticker in universe:
            results = [
                func(ticker, days_to_expiration=dte)
                for dte in range(1, 100, 7)
            ]
            monies.extend(common.as_responses(api_constructs.MoneyImplied, results))
        return monies

    def monies_implied(
        self, request: req.MoniesRequest
    ) -> Sequence[api_constructs.MoneyImplied]:
        return self._monies(request, self._generator.money_implied)

    def monies_forecast(
        self, request: req.MoniesRequest
    ) -> Sequence[api_constructs.MoneyForecast]:
        return self._monies(request, self._generator.money_forecast)

    def summaries(
        self, request: req.SummariesRequest
    ) -> Sequence[api_constructs.Summary]:
        universe = request.tickers or self._universe
        results = [self._generator.summary(ticker) for ticker in universe]
        return common.as_response(api_constructs.Summary, results)

    def core_data(self, request: req.CoreDataRequest) -> Sequence[api_constructs.Core]:
        universe = request.tickers or self._universe
        results = [self._generator.core(ticker) for ticker in universe]
        return common.as_response(api_constructs.Core, results)

    def daily_price(
        self, request: req.DailyPriceRequest
    ) -> Sequence[api_constructs.DailyPrice]:
        universe = request.tickers or self._universe
        results = [self._generator.daily_price(ticker) for ticker in universe]
        return common.as_response(api_constructs.DailyPrice, results)

    def historical_volatility(
        self, request: req.HistoricalVolatilityRequest
    ) -> Sequence[api_constructs.HistoricalVolatility]:
        universe = request.tickers or self._universe
        results = [self._generator.historical_volatility(ticker) for ticker in universe]
        return common.as_response(api_constructs.HistoricalVolatility, results)

    def dividend_history(
        self, request: req.DividendHistoryRequest
    ) -> Sequence[api_constructs.DividendHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.dividend_history(ticker) for ticker in universe]
        return common.as_response(api_constructs.DividendHistory, results)

    def earnings_history(
        self, request: req.EarningsHistoryRequest
    ) -> Sequence[api_constructs.EarningsHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.earnings_history(ticker) for ticker in universe]
        return common.as_response(api_constructs.EarningsHistory, results)

    def stock_split_history(
        self, request: req.StockSplitHistoryRequest
    ) -> Sequence[api_constructs.StockSplitHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.stock_split_history(ticker) for ticker in universe]
        return common.as_response(api_constructs.StockSplitHistory, results)

    def iv_rank(self, request: req.IvRankRequest) -> Sequence[api_constructs.IvRank]:
        universe = request.tickers or self._universe
        results = [self._generator.iv_rank(ticker) for ticker in universe]
        return common.as_response(api_constructs.IvRank, results)
