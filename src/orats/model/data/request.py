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


class _MultipleTickersTemplateRequest(DataApiRequest):
    tickers: Optional[Sequence[str]] = Field(
        None,
        alias="ticker",
        description="List of assets to retrieve.",
    )
    fields: Optional[Iterable[str]]


class _MultipleTickersHistoryTemplateRequest(_MultipleTickersTemplateRequest):
    trade_date: Optional[datetime.date] = Field(
        None,
        alias="tradeDate",
        description="The trade date to retrieve.",
    )

    _dependency_check = validator("trade_date", allow_reuse=True)(dependency_check)


class TickersRequest(_SingleTickerTemplateRequest):
    """Request duration of historical data for tickers."""


class StrikesRequest(DataApiRequest):
    """Retrieves strikes data for the given asset(s)."""

    expiration_range: Optional[BoundedRange[int]] = Field(
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


class StrikesByOptionsRequest(DataApiRequest):
    """Retrieves strikes data by ticker, expiry, and strike."""

    ticker: str = Field(
        ...,
        alias="ticker",
        description="The ticker symbol of the underlying asset.",
    )
    expiration_date: datetime.date = Field(
        ...,
        alias="expirDate",
        description="The expiration date to retrieve.",
    )
    strike: float = Field(
        ...,
        description="The strike price to retrieve.",
    )


class MoniesRequest(DataApiRequest):
    """Retrieves end of day monthly implied/forecast history data for monies."""

    tickers: Sequence[str] = Field(
        ...,
        alias="ticker",
        description="List of assets to retrieve.",
    )
    fields: Optional[Iterable[str]] = Field(
        None,
        description="The subset of fields to retrieve.",
    )


class SummariesRequest(_MultipleTickersTemplateRequest):
    """Retrieves SMV Summary data."""


class CoreDataRequest(_MultipleTickersTemplateRequest):
    """Retrieves Core history data."""


class CoreDataHistoryRequest(_MultipleTickersHistoryTemplateRequest):
    """Retrieves Core history data."""


class DailyPriceRequest(_MultipleTickersHistoryTemplateRequest):
    """Retrieves end of day daily stock price data."""


class HistoricalVolatilityRequest(_MultipleTickersHistoryTemplateRequest):
    """Retrieves historical volatility data."""


class DividendHistoryRequest(_SingleTickerTemplateRequest):
    """Retrieves dividend history data."""


class EarningsHistoryRequest(_SingleTickerTemplateRequest):
    """Retrieves earnings history data."""


class StockSplitHistoryRequest(_SingleTickerTemplateRequest):
    """Retrieves stock split history data."""


class IvRankRequest(_MultipleTickersTemplateRequest):
    """Retrieves IV rank data."""
