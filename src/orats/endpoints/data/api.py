from orats.common import get_token
from orats.endpoints.data import endpoints


class DataApi:
    """Low-level interface to the `Data API`_.

    A direct translation of the Data API that simply wraps the
    responses in structured Python objects.
    """

    def __init__(self, token: str = None):
        token = token or get_token()

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
