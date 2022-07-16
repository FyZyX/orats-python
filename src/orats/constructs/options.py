"""Higher level constructs for option contracts."""

import datetime
from typing import Optional, Sequence

from pydantic import BaseModel

import orats.endpoints.data as endpoints
from orats.constructs.assets import Asset
from orats.constructs.common import _get_token
from orats.model.data import request as req
from orats.model.data import response as res


class Quote(BaseModel):
    price: float
    size: float
    iv: Optional[float] = None


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
    price: Optional[float] = None
    spot: Optional[float] = None
    volume: Optional[int] = None
    open_interest: Optional[int] = None
    iv: Optional[float] = None
    greeks: Optional[Greeks] = None
    bid: Optional[Quote] = None
    offer: Optional[Quote] = None


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
        self._token = token or _get_token()
        self._expiration_range: Optional[str] = None
        self._delta_range: Optional[str] = None
        self._response: Optional[Sequence[res.Strike]] = None

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
                underlying=Asset(ticker=strike.underlying_symbol),
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
                underlying=Asset(ticker=strike.underlying_symbol),
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
