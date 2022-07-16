"""Higher level constructs built on top of base API."""

import datetime
from typing import Iterable, Sequence, Tuple, Collection, Union

from pydantic import BaseModel

import orats.endpoints.data as endpoints
from orats.model.data import request as req
from orats.model.data import response as res


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
        self._token = token
        self._response = None

    def _get_ticker(self):
        if self._response:
            return self._response
        endpoint = endpoints.TickersEndpoint(self._token)
        request = req.TickersRequest(ticker=self._ticker)
        # TODO: Error handling
        self._response = endpoint(request)[0]
        return self._response

    def historical_data_range(self) -> (datetime.date, datetime.date):
        """The duration of available historical data.

        Returns:
          The minimum and maximum dates of available data.
        """
        ticker = self._get_ticker()
        return ticker.min_date, ticker.max_date


class Universe:
    def __init__(self, tickers: Collection):
        self._assets: Collection[Asset] = {Asset(ticker) for ticker in tickers}


class Quote(BaseModel):
    price: float
    size: float
    iv: float = None


class Greeks(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    phi: float


class Option(BaseModel):
    underlying: Asset
    expiration: datetime.date
    strike: float
    price: float = None
    spot: float = None
    volume: int = None
    open_interest: int = None
    iv: float = None
    greeks: Greeks = None
    bid: Quote = None
    offer: Quote = None


class CallOption(Option):
    pass


class PutOption(Option):
    pass


class OptionChain:
    def __init__(self, ticker: str, token: str = None):
        """Initializes an asset object.

        Args:
          ticker:
            The ticker symbol of the underlying asset.
          token:
            API token.
        """
        self._ticker = ticker
        self._token = token
        self._expiration_range = None
        self._delta_range = None
        self._response = None

    def _get_strikes(self, trade_date: datetime.date = None):
        if self._response:
            return self._response

        endpoint = endpoints.StrikesEndpoint(self._token)
        request = req.StrikesRequest(
            tickers=self._ticker,
            trade_date=trade_date,
            expiration_range=self._expiration_range,
            delta_range=self._delta_range,
        )

        self._response = endpoint(request)
        return self._response

    def filter_by_days_to_expiration(
        self,
        lower_bound: int = None,
        upper_bound: int = None,
    ):
        """Keep only those options within the specified range of days to expiration.

        Args:
          lower_bound:
            Smallest number of days to expiration allowed.
            If not specified, no bound will be set.
          upper_bound:
            Largest number of days to expiration allowed.
            If not specified, no bound will be set.

        Returns:
          A list of strikes for each specified asset.
        """
        self._expiration_range = ",".join(map(str, (lower_bound, upper_bound)))

    def filter_by_delta(
        self,
        lower_bound: float = None,
        upper_bound: float = None,
    ):
        self._delta_range = ",".join(map(str, (lower_bound, upper_bound)))

    def options(self, trade_date: datetime.date = None):
        # https://blog.orats.com/option-greeks-are-the-same-for-calls-and-puts
        return self._get_strikes(trade_date)

    def calls(self, trade_date: datetime.date = None):
        return [
            CallOption(
                underlying=Asset(strike.underlying_symbol),
                expiration=strike.expiration_date,
                strike=strike.strike,
                price=strike.call_value,
                spot=strike.spot_price,
                volume=strike.call_volume,
                open_interest=strike.call_open_interest,
                iv=strike.iv,
                greeks=Greeks(
                    delta=strike.delta,
                    gamma=strike.gamma,
                    theta=strike.theta,
                    vega=strike.vega,
                    rho=strike.rho,
                    phi=strike.phi,
                ),
                bid=Quote(
                    price=strike.call_bid_price,
                    size=strike.call_bid_size,
                    iv=strike.call_bid_iv,
                ),
                offer=Quote(
                    price=strike.call_ask_price,
                    size=strike.call_ask_size,
                    iv=strike.call_ask_iv,
                ),
            )
            for strike in self._get_strikes(trade_date)
        ]

    def puts(self, trade_date: datetime.date = None):
        return [
            PutOption(
                underlying=Asset(strike.underlying_symbol),
                expiration=strike.expiration_date,
                strike=strike.strike,
                price=strike.put_value,
                spot=strike.spot_price,
                volume=strike.put_volume,
                open_interest=strike.put_open_interest,
                iv=strike.iv,
                greeks=Greeks(
                    delta=strike.delta - 1,
                    gamma=strike.gamma,
                    theta=strike.theta,
                    vega=strike.vega,
                    rho=strike.rho,
                    phi=strike.phi,
                ),
                bid=Quote(
                    price=strike.put_bid_price,
                    size=strike.put_bid_size,
                    iv=strike.put_bid_iv,
                ),
                offer=Quote(
                    price=strike.put_ask_price,
                    size=strike.put_ask_size,
                    iv=strike.put_ask_iv,
                ),
            )
            for strike in self._get_strikes(trade_date)
        ]
