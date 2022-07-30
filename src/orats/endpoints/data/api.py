from orats.common import get_token
from orats.endpoints.data import endpoints


class DataApi:
    """Low-level interface to the `Data API`_.

    A direct translation of the Data API that simply wraps the
    responses in structured Python objects.
    """

    def __init__(self, token: str = None, mock: bool = False):
        token = token or get_token()

        self.tickers = endpoints.TickersEndpoint(token, mock=mock)
        self.strikes = endpoints.StrikesEndpoint(token, mock=mock)
        self.strikes_by_options = endpoints.StrikesByOptionsEndpoint(token, mock=mock)
        self.monies_implied = endpoints.MoniesImpliedEndpoint(token, mock=mock)
        self.monies_forecast = endpoints.MoniesForecastEndpoint(token, mock=mock)
        self.summaries = endpoints.SummariesEndpoint(token, mock=mock)
        self.core_data = endpoints.CoreDataEndpoint(token, mock=mock)
        self.daily_price = endpoints.DailyPriceEndpoint(token, mock=mock)
        self.historical_volatility = endpoints.HistoricalVolatilityEndpoint(
            token, mock=mock
        )
        self.dividend_history = endpoints.DividendHistoryEndpoint(token, mock=mock)
        self.earnings_history = endpoints.EarningsHistoryEndpoint(token, mock=mock)
        self.stock_split_history = endpoints.StockSplitHistoryEndpoint(token, mock=mock)
        self.iv_rank = endpoints.IvRankEndpoint(token, mock=mock)
