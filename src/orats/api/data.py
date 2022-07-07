import datetime
from typing import Any, Iterable, Mapping, Sequence

import httpx

from orats.model.core import Core
from orats.model.money import MoneyForecast, MoneyImplied
from orats.model.strike import Strike
from orats.model.summary import SmvSummary
from orats.model.underlying import (
    Ticker,
    DailyPrice,
    DividendHistory,
    EarningsHistory,
    StockSplitHistory,
)
from orats.model.volatility import HistoricalVolatility, IvRank


class DataApi:
    _base_url = "https://api.orats.io/datav2"

    def __init__(self, token):
        self._token = token

    def _url(self, path):
        return "/".join((self._base_url, path))

    def _update_params(self, params: Mapping[str, Any]):
        updated_params = dict(token=self._token)
        for key, param in params.items():
            if param is None:
                continue
            updated_params[key] = param
        return updated_params

    def _get(self, path: str, **params: Any):
        response = httpx.get(
            url=self._url(path),
            params=self._update_params(params),
        )
        return response.json()["data"]

    def tickers(self, symbol: str = None) -> Sequence[Ticker]:
        data = self._get("tickers", ticker=symbol)
        return [Ticker(**t) for t in data]

    def strikes(
        self,
        *symbols: str,
        delta: float = None,
        days_to_expiration: int = None,
        fields: Iterable[str] = None,
    ) -> Sequence[Strike]:
        data = self._get(
            "strikes",
            ticker=",".join(symbols),
            fields=fields,
            dte=days_to_expiration,
            delta=delta,
        )
        return [Strike(**s) for s in data]

    def strikes_history(
        self,
        *symbols: str,
        trade_date: datetime.date,
        fields: Iterable[str] = None,
        days_to_expiration: int = None,
        delta: float = None,
    ) -> Sequence[Strike]:
        data = self._get(
            "hist/strikes",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
            dte=days_to_expiration,
            delta=delta,
        )
        return [Strike(**s) for s in data]

    def strikes_by_options(
        self,
        symbol: str,
        strike: float,
        expiration_date: datetime.date,
    ) -> Sequence[Strike]:
        data = self._get(
            "strikes/options",
            ticker=symbol,
            expirDate=expiration_date,
            strike=strike,
        )
        return [Strike(**s) for s in data]

    def strikes_history_by_options(
        self,
        symbol: str,
        strike: float,
        expiration_date: datetime.date,
        trade_date: datetime.date = None,
    ) -> Sequence[Strike]:
        data = self._get(
            "hist/strikes/options",
            ticker=symbol,
            tradeDate=trade_date,
            expirDate=expiration_date,
            strike=strike,
        )
        return [Strike(**s) for s in data]

    def monies_implied(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyImplied]:
        data = self._get(
            "monies/implied",
            ticker=",".join(symbols),
            fields=fields,
        )
        return [MoneyImplied(**m) for m in data]

    def monies_forecast(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyForecast]:
        data = self._get(
            "monies/forecast",
            ticker=",".join(symbols),
            fields=fields,
        )
        return [MoneyForecast(**m) for m in data]

    def monies_implied_history(
        self,
        *symbols: str,
        trade_date: datetime.date,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyImplied]:
        data = self._get(
            "hist/monies/implied",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
        return [MoneyImplied(**m) for m in data]

    def monies_forecast_history(
        self,
        *symbols: str,
        trade_date: datetime.date,
        fields: Iterable[str] = None,
    ) -> Sequence[MoneyForecast]:
        data = self._get(
            "hist/monies/forecast",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
        return [MoneyForecast(**m) for m in data]

    def summaries(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[SmvSummary]:
        data = self._get(
            "summaries",
            ticker=",".join(symbols),
            fields=fields,
        )
        return [SmvSummary(**s) for s in data]

    def summaries_history(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[SmvSummary]:
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/summaries",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
        return [SmvSummary(**m) for m in data]

    def core_data(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[Core]:
        data = self._get(
            "cores",
            ticker=",".join(symbols),
            fields=fields,
        )
        return [Core(**c) for c in data]

    def core_data_history(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[Core]:
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/cores",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
        return [Core(**c) for c in data]

    def daily_price(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[DailyPrice]:
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/dailies",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
        return [DailyPrice(**p) for p in data]

    def historical_volatility(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[HistoricalVolatility]:
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/hvs",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
        return [HistoricalVolatility(**hv) for hv in data]

    def dividend_history(
        self,
        *symbols: str,
    ) -> Sequence[DividendHistory]:
        data = self._get(
            "hist/divs",
            ticker=",".join(symbols),
        )
        return [DividendHistory(**d) for d in data]

    def earnings_history(
        self,
        *symbols: str,
    ) -> Sequence[EarningsHistory]:
        data = self._get(
            "hist/earnings",
            ticker=",".join(symbols),
        )
        return [EarningsHistory(**e) for e in data]

    def stock_split_history(
        self,
        *symbols: str,
    ) -> Sequence[StockSplitHistory]:
        data = self._get(
            "hist/splits",
            ticker=",".join(symbols),
        )
        return [StockSplitHistory(**e) for e in data]

    def iv_rank(
        self,
        *symbols: str,
        fields: Iterable[str] = None,
    ) -> Sequence[IvRank]:
        data = self._get(
            "ivrank",
            ticker=",".join(symbols),
            fields=fields,
        )
        return [IvRank(**e) for e in data]

    def iv_rank_history(
        self,
        *symbols: str,
        trade_date: datetime.date = None,
        fields: Iterable[str] = None,
    ) -> Sequence[IvRank]:
        assert len(symbols) and trade_date is not None
        data = self._get(
            "hist/ivrank",
            ticker=",".join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
        return [IvRank(**e) for e in data]
