"""Higher level constructs for underlying assets."""

import datetime
from typing import Tuple, Collection, Optional

from pydantic import BaseModel, Field

import orats.endpoints.data as endpoints
from orats.constructs.common import _get_token
from orats.model.data import request as req
from orats.model.data import response as res


class Asset(BaseModel):
    """Represents the underlying asset of an option contract."""

    ticker: str = Field(..., description="The ticker symbol of the underlying asset.")
    token: str = Field(_get_token(), description="API token.")
    _response: Optional[res.TickerResponse] = None

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
