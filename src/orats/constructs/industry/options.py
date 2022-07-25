"""Higher level constructs for option contracts."""

import datetime
from typing import Optional, Sequence

from orats.constructs.api import data as constructs
from orats.constructs.common import IndustryConstruct
from orats.constructs.industry.assets import Asset
from orats.endpoints.data import endpoints, request as req


class Quote(IndustryConstruct):
    price: float
    size: float
    iv: Optional[float] = None


class Greeks(IndustryConstruct):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    phi: float


class Option(IndustryConstruct):
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


class OptionChain(IndustryConstruct):
    ticker: str
    _expiration_range: Optional[str] = None
    _delta_range: Optional[str] = None
    _cache: Optional[Sequence[constructs.Strike]] = None

    def _get_strikes(self, trade_date: datetime.date = None):
        if self._cache:
            return self._cache

        endpoint = endpoints.StrikesEndpoint(self._token)
        request = req.StrikesRequest(
            tickers=self.ticker,
            trade_date=trade_date,
            expiration_range=self._expiration_range,
            delta_range=self._delta_range,
        )

        self._cache = endpoint(request)
        return self._cache

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


class VolatilitySurface(IndustryConstruct):
    ticker: str
    _cache: Optional[Sequence[constructs.MoneyImplied]] = None

    def _get_monies(self, trade_date: datetime.date = None):
        if self._cache:
            return self._cache

        endpoint = endpoints.MoniesImpliedEndpoint(self._token)
        request = req.MoniesRequest(
            tickers=self.ticker,
            trade_date=trade_date,
        )

        self._cache = endpoint(request)
        return self._cache
