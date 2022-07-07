import datetime

from pydantic import Field

from .response import OratsResponse


class Strike(OratsResponse):
    underlying_symbol: str = Field(..., alias="ticker")
    trade_date: datetime.date = Field(..., alias="tradeDate")
    expiration_date: datetime.date = Field(..., alias="expirDate")
    days_to_expiration: int = Field(..., alias="dte")
    strike: float
    spot_price: float = Field(..., alias="spotPrice")
    underlying_price: float = Field(..., alias="stockPrice")
    iv: float = Field(..., alias="smvVol")
    external_iv: float = Field(..., alias="extSmvVol")
    call_volume: int = Field(..., alias="callVolume")
    call_open_interest: int = Field(..., alias="callOpenInterest")
    call_bid_size: int = Field(..., alias="callBidSize")
    call_ask_size: int = Field(..., alias="callAskSize")
    call_bid_price: float = Field(..., alias="callBidPrice")
    call_ask_price: float = Field(..., alias="callAskPrice")
    call_value: float = Field(..., alias="callValue")
    call_bid_iv: float = Field(..., alias="callBidIv")
    call_mid_iv: float = Field(..., alias="callMidIv")
    call_ask_iv: float = Field(..., alias="callAskIv")
    external_call_value: float = Field(..., alias="extCallValue")
    put_volume: int = Field(..., alias="putVolume")
    put_open_interest: int = Field(..., alias="putOpenInterest")
    put_bid_size: int = Field(..., alias="putBidSize")
    put_ask_size: int = Field(..., alias="putAskSize")
    put_bid_price: float = Field(..., alias="putBidPrice")
    put_ask_price: float = Field(..., alias="putAskPrice")
    put_value: float = Field(..., alias="putValue")
    external_put_value: float = Field(..., alias="extPutValue")
    put_bid_iv: float = Field(..., alias="putBidIv")
    put_mid_iv: float = Field(..., alias="putMidIv")
    put_ask_iv: float = Field(..., alias="putAskIv")
    residual_rate: float = Field(..., alias="residualRate")
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    phi: float
    driftless_theta: float = Field(..., alias="driftlessTheta")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")
