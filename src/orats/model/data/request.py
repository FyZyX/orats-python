import datetime
import sys
from numbers import Number
from typing import (
    Any,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeAlias,
    Union,
    TypeVar,
)

from pydantic import BaseModel, Field, validator

EllipsisType = Type[Any]
if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from types import EllipsisType
A = TypeVar("A", bound=Number)
BoundedRange: TypeAlias = Tuple[Union[A, EllipsisType], Union[A, EllipsisType]]


def dependency_check(v, values):
    if values.get("tickers") is None and v is None:
        raise ValueError("one of `tickers` or `trade_date` is required")
    return v


class DataApiRequest(BaseModel):
    class Config:
        allow_population_by_field_name = True
        # TODO: Kinda hacky way to use Ellipsis in DTE and delta range filters.
        arbitrary_types_allowed = True


class _SingleTickerTemplateRequest(DataApiRequest):
    ticker: str = Field(..., alias="ticker")


class DataHistoryApiRequest(DataApiRequest):
    trade_date: Optional[datetime.date] = Field(None, alias="tradeDate")


class _MultipleTickersTemplateRequest(DataHistoryApiRequest):
    tickers: Sequence[str] = Field(None, alias="ticker")
    fields: Optional[Iterable[str]]


class _MultipleTickersDependentTemplateRequest(DataHistoryApiRequest):
    tickers: Optional[Sequence[str]] = Field(None, alias="ticker")
    fields: Optional[Iterable[str]]

    _dependency_check = validator("trade_date", allow_reuse=True)(dependency_check)


class TickersRequest(_SingleTickerTemplateRequest):
    pass


class StrikesRequest(_MultipleTickersTemplateRequest):
    expiration_range: Optional[BoundedRange[int]] = Field(None, alias="dte")
    delta_range: Optional[BoundedRange[float]] = Field(None, alias="delta")


class StrikesByOptionsRequest(_SingleTickerTemplateRequest):
    trade_date: datetime.date = Field(None, alias="tradeDate")
    expiration_date: datetime.date = Field(..., alias="expirDate")
    strike: float


class MoniesRequest(_MultipleTickersTemplateRequest):
    pass


class SummariesRequest(_MultipleTickersDependentTemplateRequest):
    pass


class CoreDataRequest(_MultipleTickersDependentTemplateRequest):
    pass


class DailyPriceRequest(_MultipleTickersDependentTemplateRequest):
    pass


class HistoricalVolatilityRequest(_MultipleTickersDependentTemplateRequest):
    pass


class DividendHistoryRequest(_SingleTickerTemplateRequest):
    pass


class EarningsHistoryRequest(_SingleTickerTemplateRequest):
    pass


class StockSplitHistoryRequest(_SingleTickerTemplateRequest):
    pass


class IvRankRequest(_MultipleTickersDependentTemplateRequest):
    pass
