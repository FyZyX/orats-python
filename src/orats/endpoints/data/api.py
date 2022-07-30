from orats.common import get_token
from orats.endpoints.data import endpoints


class DataApi:
    """Low-level interface to the `Data API`_.

    A direct translation of the Data API that simply wraps the
    responses in structured Python objects.
    """

    def __init__(self, token: str = None, mock=False):
        token = token or get_token()

        if not mock:
            self.tickers = endpoints.TickersEndpoint(token)
            self.strikes = endpoints.StrikesEndpoint(token)
            self.strikes_by_options = endpoints.StrikesByOptionsEndpoint(token)
            self.monies_implied = endpoints.MoniesImpliedEndpoint(token)
            self.monies_forecast = endpoints.MoniesForecastEndpoint(token)
            self.summaries = endpoints.SummariesEndpoint(token)
            self.core_data = endpoints.CoreDataEndpoint(token)
            self.daily_price = endpoints.DailyPriceEndpoint(token)
            self.historical_volatility = endpoints.HistoricalVolatilityEndpoint(token)
            self.dividend_history = endpoints.DividendHistoryEndpoint(token)
            self.earnings_history = endpoints.EarningsHistoryEndpoint(token)
            self.stock_split_history = endpoints.StockSplitHistoryEndpoint(token)
            self.iv_rank = endpoints.IvRankEndpoint(token)
        else:
            from orats.sandbox.api.data import FakeDataApi

            data_generator = FakeDataApi()
            self.tickers = data_generator.tickers
            self.strikes = data_generator.strikes
            self.strikes_by_options = data_generator.strikes_by_options
            self.monies_implied = data_generator.monies_implied
            self.monies_forecast = data_generator.monies_forecast
            self.summaries = data_generator.summaries
            self.core_data = data_generator.core_data
            self.daily_price = data_generator.daily_price
            self.historical_volatility = data_generator.historical_volatility
            self.dividend_history = data_generator.dividend_history
            self.earnings_history = data_generator.earnings_history
            self.stock_split_history = data_generator.stock_split_history
            self.iv_rank = data_generator.iv_rank
