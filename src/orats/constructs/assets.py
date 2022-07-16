"""Higher level constructs for underlying assets."""

import datetime
from typing import Tuple, Collection

import orats.endpoints.data as endpoints
from orats.constructs.common import _get_token
from orats.model.data import request as req


class Asset:
    """Represents the underlying asset of an option contract."""

    def __init__(self, ticker: str, token: str = None):
        """Initializes an asset object.

        Args:
          ticker:
            The ticker symbol of the underlying asset.
          token:
            API token.
        """
        self._ticker = ticker
        self._token = token or _get_token()
        self._response = None

    def _get_ticker(self):
        if self._response:
            return self._response
        endpoint = endpoints.TickersEndpoint(self._token)
        request = req.TickersRequest(ticker=self._ticker)
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
        self._assets: Collection[Asset] = {Asset(ticker) for ticker in tickers}
