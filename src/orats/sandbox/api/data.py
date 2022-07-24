import datetime
from typing import Dict, Any, TypeAlias, Sequence

from orats.constructs.api.data import request as req
from orats.constructs.api.data import response as res
from orats.sandbox import common
from orats.sandbox.api.generator import FakeDataGenerator

Json: TypeAlias = Dict[str, Any]


def _resource(url):
    return "/".join(url.split("://")[1].split("/")[2:])


def fake_api_request(url, params=None, body=None, count=1):
    data_generator = FakeDataGenerator()
    data_definition = data_generator.get_data_definition(_resource(url))
    return {"data": [data_definition() for _ in range(count)]}


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

    def tickers(self, request: req.TickersRequest) -> Sequence[res.Ticker]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.ticker(ticker) for ticker in universe]
        return common.as_response(res.Ticker, results)

    def strikes(self, request: req.StrikesRequest) -> Sequence[res.Strike]:
        universe = request.tickers or self._universe
        results = [self._generator.strike(ticker) for ticker in universe]
        return common.as_response(res.Strike, results)

    def strikes_by_options(
        self, *requests: req.StrikesByOptionsRequest
    ) -> Sequence[res.Strike]:
        results = [self._generator.strike(request.ticker) for request in requests]
        return common.as_response(res.Strike, results)

    def monies_implied(self, request: req.MoniesRequest) -> Sequence[res.MoneyImplied]:
        universe = request.tickers or self._universe
        results = [self._generator.money_implied(ticker) for ticker in universe]
        return common.as_response(res.MoneyImplied, results)

    def monies_forecast(
        self, request: req.MoniesRequest
    ) -> Sequence[res.MoneyForecast]:
        universe = request.tickers or self._universe
        results = [self._generator.money_forecast(ticker) for ticker in universe]
        return common.as_response(res.MoneyForecast, results)

    def summaries(self, request: req.SummariesRequest) -> Sequence[res.SmvSummary]:
        universe = request.tickers or self._universe
        results = [self._generator.summary(ticker) for ticker in universe]
        return common.as_response(res.SmvSummary, results)

    def core_data(self, request: req.CoreDataRequest) -> Sequence[res.Core]:
        universe = request.tickers or self._universe
        results = [self._generator.core(ticker) for ticker in universe]
        return common.as_response(res.Core, results)

    def daily_price(self, request: req.DailyPriceRequest) -> Sequence[res.DailyPrice]:
        universe = request.tickers or self._universe
        results = [self._generator.daily_price(ticker) for ticker in universe]
        return common.as_response(res.DailyPrice, results)

    def historical_volatility(
        self, request: req.HistoricalVolatilityRequest
    ) -> Sequence[res.HistoricalVolatility]:
        universe = request.tickers or self._universe
        results = [self._generator.historical_volatility(ticker) for ticker in universe]
        return common.as_response(res.HistoricalVolatility, results)

    def dividend_history(
        self, request: req.DividendHistoryRequest
    ) -> Sequence[res.DividendHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.dividend_history(ticker) for ticker in universe]
        return common.as_response(res.DividendHistory, results)

    def earnings_history(
        self, request: req.EarningsHistoryRequest
    ) -> Sequence[res.EarningsHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.earnings_history(ticker) for ticker in universe]
        return common.as_response(res.EarningsHistory, results)

    def stock_split_history(
        self, request: req.StockSplitHistoryRequest
    ) -> Sequence[res.StockSplitHistory]:
        if request.ticker:
            universe = [request.ticker]
        else:
            universe = self._universe
        results = [self._generator.stock_split_history(ticker) for ticker in universe]
        return common.as_response(res.StockSplitHistory, results)

    def iv_rank(self, request: req.IvRankRequest) -> Sequence[res.IvRank]:
        universe = request.tickers or self._universe
        results = [self._generator.iv_rank(ticker) for ticker in universe]
        return common.as_response(res.IvRank, results)
