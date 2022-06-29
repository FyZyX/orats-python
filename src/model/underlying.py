import datetime

from pydantic import BaseModel, Field


class Ticker(BaseModel):
    underlying_symbol: str = Field(..., alias='ticker')
    min_date: datetime.date = Field(..., alias='min')
    max_date: datetime.date = Field(..., alias='max')


class DailyPrice(BaseModel):
    underlying_symbol: str = Field(..., alias='ticker')
    trade_date: datetime.date = Field(..., alias='tradeDate')
    open: float = Field(..., alias='open')
    high: float = Field(..., alias='hiPx')
    low: float = Field(..., alias='loPx')
    close: float = Field(..., alias='clsPx')
    unadjusted_open: float = Field(..., alias='unadjOpen')
    unadjusted_high: float = Field(..., alias='unadjHiPx')
    unadjusted_low: float = Field(..., alias='unadjLoPx')
    unadjusted_close: float = Field(..., alias='unadjClsPx')
    updated_at: datetime.datetime = Field(..., alias='updatedAt')


class DividendHistory(BaseModel):
    underlying_symbol: str = Field(..., alias='ticker')
    ex_dividend_date: datetime.date = Field(..., alias='exDate')
    dividend_amount: float = Field(..., alias='divAmt')
    dividend_frequency: int = Field(..., alias='divFreq')
    declared_date: datetime.date = Field(..., alias='declaredDate')


class EarningsHistory(BaseModel):
    underlying_symbol: str = Field(..., alias='ticker')
    earnings_date: datetime.date = Field(..., alias='earnDate')
    time_of_day_announced: int = Field(..., alias='anncTod')
    updated_at: datetime.date = Field(..., alias='updatedAt')


class StockSplitHistory(BaseModel):
    underlying_symbol: str = Field(..., alias='ticker')
    split_date: datetime.date = Field(..., alias='splitDate')
    divisor: float
