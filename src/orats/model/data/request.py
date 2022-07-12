import datetime
from typing import Sequence, Tuple, Iterable, Optional, Union

from pydantic import BaseModel, Field, validator


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


class _MultipleTickersTemplateRequest(DataApiRequest):
    tickers: Optional[Sequence[str]] = Field(None, alias="ticker")
    fields: Optional[Iterable[str]]


class _MultipleTickersHistoryTemplateRequest(_MultipleTickersTemplateRequest):
    trade_date: Optional[datetime.date] = Field(None, alias="tradeDate")

    _dependency_check = validator("trade_date", allow_reuse=True)(dependency_check)


class TickersRequest(_SingleTickerTemplateRequest):
    pass


class StrikesRequest(DataApiRequest):
    tickers: Sequence[str] = Field(..., alias="ticker")
    fields: Optional[Iterable[str]]
    expiration_range: Optional[
        Tuple[Union[int, type(Ellipsis)], Union[int, type(Ellipsis)]]
    ] = Field(None, alias="dte")
    delta_range: Optional[
        Tuple[Union[float, type(Ellipsis)], Union[float, type(Ellipsis)]]
    ] = Field(None, alias="delta")


class StrikesHistoryRequest(StrikesRequest):
    trade_date: datetime.date = Field(..., alias="tradeDate")


class StrikesByOptionsRequest(DataApiRequest):
    ticker: str = Field(..., alias="ticker")
    expiration_date: datetime.date = Field(..., alias="expirDate")
    strike: float


class StrikesHistoryByOptionsRequest(StrikesByOptionsRequest):
    trade_date: datetime.date = Field(..., alias="tradeDate")


class MoniesRequest(DataApiRequest):
    tickers: Sequence[str] = Field(..., alias="ticker")
    fields: Optional[Iterable[str]]


class MoniesHistoryRequest(MoniesRequest):
    trade_date: datetime.date = Field(..., alias="tradeDate")


class SummariesRequest(_MultipleTickersTemplateRequest):
    pass


class SummariesHistoryRequest(_MultipleTickersHistoryTemplateRequest):
    pass


class CoreDataRequest(_MultipleTickersTemplateRequest):
    pass


class CoreDataHistoryRequest(_MultipleTickersHistoryTemplateRequest):
    pass


class DailyPriceRequest(_MultipleTickersHistoryTemplateRequest):
    pass


class HistoricalVolatilityRequest(_MultipleTickersHistoryTemplateRequest):
    pass


class DividendHistoryRequest(_SingleTickerTemplateRequest):
    pass


class EarningsHistoryRequest(_SingleTickerTemplateRequest):
    pass


class StockSplitHistoryRequest(_SingleTickerTemplateRequest):
    pass


class IvRankRequest(_MultipleTickersTemplateRequest):
    pass


class IvRankHistoryRequest(_MultipleTickersHistoryTemplateRequest):
    pass
