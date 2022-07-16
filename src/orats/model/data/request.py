import datetime
from typing import (
    Iterable,
    Optional,
    Sequence,
)

from pydantic import BaseModel, Field, validator


def dependency_check(v, values):
    if values.get("tickers") is None and v is None:
        raise ValueError("one of `tickers` or `trade_date` is required")
    return v


class DataApiRequest(BaseModel):
    class Config:
        allow_population_by_field_name = True


class _SingleTickerTemplateRequest(DataApiRequest):
    ticker: str = Field(
        ...,
        alias="ticker",
        description="The ticker symbol of the underlying asset.",
    )


class DataHistoryApiRequest(DataApiRequest):
    trade_date: Optional[datetime.date] = Field(
        None,
        alias="tradeDate",
        description="The trade date to retrieve.",
    )
    fields: Optional[Iterable[str]]


class _MultipleTickersTemplateRequest(DataHistoryApiRequest):
    tickers: Sequence[str] = Field(
        None,
        alias="ticker",
        description="List of assets to retrieve.",
    )
    fields: Optional[Iterable[str]]


class _MultipleTickersDependentTemplateRequest(DataHistoryApiRequest):
    tickers: Optional[Sequence[str]] = Field(
        None,
        alias="ticker",
        description="List of assets to retrieve.",
    )
    fields: Optional[Iterable[str]]

    _dependency_check = validator("trade_date", allow_reuse=True)(dependency_check)


class TickersRequest(_SingleTickerTemplateRequest):
    """Request duration of historical data for tickers."""


class StrikesRequest(_MultipleTickersTemplateRequest):
    """Retrieves strikes data for the given asset(s)."""

    expiration_range: Optional[str] = Field(
        None,
        alias="dte",
        description="Filters results to a range of days to expiration."
        "Specified as a comma separated pair of integers."
        "To ignore an upper/lower bound, leave the value blank."
        "Examples: ``30,45``, ``30,`` == ``30``, ``,45``",
    )
    delta_range: Optional[str] = Field(
        None,
        alias="delta",
        description="Filters results to a range of delta values."
        "Specified as a comma separated pair of floating point numbers."
        "To ignore an upper/lower bound, leave the value blank."
        "Examples: ``.30,.45``, ``.30,`` == ``.30``, ``,.45``",
    )


class StrikesByOptionsRequest(_SingleTickerTemplateRequest):
    """Retrieves strikes data by ticker, expiry, and strike."""

    expiration_date: datetime.date = Field(
        ...,
        alias="expirDate",
        description="The expiration date to retrieve.",
    )
    strike: float = Field(
        ...,
        description="The strike price to retrieve.",
    )


class MoniesRequest(_MultipleTickersTemplateRequest):
    """Retrieves end of day monthly implied/forecast history data for monies."""


class SummariesRequest(_MultipleTickersDependentTemplateRequest):
    """Retrieves SMV Summary data."""


class CoreDataRequest(_MultipleTickersDependentTemplateRequest):
    """Retrieves Core history data."""


class CoreDataHistoryRequest(_MultipleTickersDependentTemplateRequest):
    """Retrieves Core history data."""


class DailyPriceRequest(_MultipleTickersDependentTemplateRequest):
    """Retrieves end of day daily stock price data."""


class HistoricalVolatilityRequest(_MultipleTickersDependentTemplateRequest):
    """Retrieves historical volatility data."""


class DividendHistoryRequest(_SingleTickerTemplateRequest):
    """Retrieves dividend history data."""


class EarningsHistoryRequest(_SingleTickerTemplateRequest):
    """Retrieves earnings history data."""


class StockSplitHistoryRequest(_SingleTickerTemplateRequest):
    """Retrieves stock split history data."""


class IvRankRequest(_MultipleTickersDependentTemplateRequest):
    """Retrieves IV rank data."""
