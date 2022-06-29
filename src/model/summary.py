import datetime

from pydantic import BaseModel, Field


class SmvSummary(BaseModel):
    underlying_symbol: str = Field(..., alias='ticker')
    trade_date: datetime.date = Field(..., alias='tradeDate')
    underlying_price: float = Field(..., alias='stockPrice')
    annual_dividend: float = Field(..., alias='annActDiv')
    annual_implied_dividend: float = Field(..., alias='annIdiv')
    next_dividend: float = Field(..., alias='nextDiv')
    implied_next_dividend: float = Field(..., alias='impliedNextDiv')
    hard_to_borrow_30_days: float = Field(..., alias='borrow30')
    hard_to_borrow_2_years: float = Field(..., alias='borrow2y')
    confidence: float
    iv_ex_earnings_10_day: float = Field(..., alias='exErnIv10d')
    iv_ex_earnings_20_day: float = Field(..., alias='exErnIv20d')
    iv_ex_earnings_30_day: float = Field(..., alias='exErnIv30d')
    iv_ex_earnings_60_day: float = Field(..., alias='exErnIv60d')
    iv_ex_earnings_90_day: float = Field(..., alias='exErnIv90d')
    iv_ex_earnings_180_day: float = Field(..., alias='exErnIv6m')
    iv_ex_earnings_365_day: float = Field(..., alias='exErnIv1y')
    implied_earnings_effect: float = Field(..., alias='ieeEarnEffect')
    implied_move: float = Field(..., alias='impliedMove')
    implied_earnings_move: float = Field(..., alias='impliedEarningsMove')
    iv_interpolated_10_day: float = Field(..., alias='iv10d')
    iv_interpolated_20_day: float = Field(..., alias='iv20d')
    iv_interpolated_30_day: float = Field(..., alias='iv30d')
    iv_interpolated_60_day: float = Field(..., alias='iv60d')
    iv_interpolated_90_day: float = Field(..., alias='iv90d')
    iv_interpolated_180_day: float = Field(..., alias='iv6m')
    iv_interpolated_365_day: float = Field(..., alias='iv1y')
    market_width_30_day: float = Field(..., alias='mwAdj30')
    market_width_2_year: float = Field(..., alias='mwAdj2y')
    derivative_30_day: float = Field(..., alias='rDrv30')
    derivative_2_year: float = Field(..., alias='rDrv2y')
    slope_30_day: float = Field(..., alias='rSlp30')
    slope_2_year: float = Field(..., alias='rSlp2y')
    iv_30_day: float = Field(..., alias='rVol30')
    iv_2_year: float = Field(..., alias='rVol2y')
    ignore_price: float = Field(..., alias='rip')
    risk_free_rate_30_day: float = Field(..., alias='riskFree30')
    risk_free_rate_2_year: float = Field(..., alias='riskFree2y')
    skewing: float
    contango: float
    total_error_confidence: float = Field(..., alias='totalErrorConf')
    iv_5_delta_10_day: float = Field(..., alias='dlt5Iv10d')
    iv_5_delta_20_day: float = Field(..., alias='dlt5Iv20d')
    iv_5_delta_30_day: float = Field(..., alias='dlt5Iv30d')
    iv_5_delta_60_day: float = Field(..., alias='dlt5Iv60d')
    iv_5_delta_90_day: float = Field(..., alias='dlt5Iv90d')
    iv_5_delta_180_day: float = Field(..., alias='dlt5Iv6m')
    iv_5_delta_365_day: float = Field(..., alias='dlt5Iv1y')
    iv_ex_earnings_5_delta_10_day: float = Field(..., alias='exErnDlt5Iv10d')
    iv_ex_earnings_5_delta_20_day: float = Field(..., alias='exErnDlt5Iv20d')
    iv_ex_earnings_5_delta_30_day: float = Field(..., alias='exErnDlt5Iv30d')
    iv_ex_earnings_5_delta_60_day: float = Field(..., alias='exErnDlt5Iv60d')
    iv_ex_earnings_5_delta_90_day: float = Field(..., alias='exErnDlt5Iv90d')
    iv_ex_earnings_5_delta_180_day: float = Field(..., alias='exErnDlt5Iv6m')
    iv_ex_earnings_5_delta_365_day: float = Field(..., alias='exErnDlt5Iv1y')
    iv_25_delta_10_day: float = Field(..., alias='dlt25Iv10d')
    iv_25_delta_20_day: float = Field(..., alias='dlt25Iv20d')
    iv_25_delta_30_day: float = Field(..., alias='dlt25Iv30d')
    iv_25_delta_60_day: float = Field(..., alias='dlt25Iv60d')
    iv_25_delta_90_day: float = Field(..., alias='dlt25Iv90d')
    iv_25_delta_180_day: float = Field(..., alias='dlt25Iv6m')
    iv_25_delta_365_day: float = Field(..., alias='dlt25Iv1y')
    iv_ex_earnings_25_delta_10_day: float = Field(..., alias='exErnDlt25Iv10d')
    iv_ex_earnings_25_delta_20_day: float = Field(..., alias='exErnDlt25Iv20d')
    iv_ex_earnings_25_delta_30_day: float = Field(..., alias='exErnDlt25Iv30d')
    iv_ex_earnings_25_delta_60_day: float = Field(..., alias='exErnDlt25Iv60d')
    iv_ex_earnings_25_delta_90_day: float = Field(..., alias='exErnDlt25Iv90d')
    iv_ex_earnings_25_delta_180_day: float = Field(..., alias='exErnDlt25Iv6m')
    iv_ex_earnings_25_delta_365_day: float = Field(..., alias='exErnDlt25Iv1y')
    iv_75_delta_10_day: float = Field(..., alias='dlt75Iv10d')
    iv_75_delta_20_day: float = Field(..., alias='dlt75Iv20d')
    iv_75_delta_30_day: float = Field(..., alias='dlt75Iv30d')
    iv_75_delta_60_day: float = Field(..., alias='dlt75Iv60d')
    iv_75_delta_90_day: float = Field(..., alias='dlt75Iv90d')
    iv_75_delta_180_day: float = Field(..., alias='dlt75Iv6m')
    iv_75_delta_365_day: float = Field(..., alias='dlt75Iv1y')
    iv_ex_earnings_75_delta_10_day: float = Field(..., alias='exErnDlt75Iv10d')
    iv_ex_earnings_75_delta_20_day: float = Field(..., alias='exErnDlt75Iv20d')
    iv_ex_earnings_75_delta_30_day: float = Field(..., alias='exErnDlt75Iv30d')
    iv_ex_earnings_75_delta_60_day: float = Field(..., alias='exErnDlt75Iv60d')
    iv_ex_earnings_75_delta_90_day: float = Field(..., alias='exErnDlt75Iv90d')
    iv_ex_earnings_75_delta_180_day: float = Field(..., alias='exErnDlt75Iv6m')
    iv_ex_earnings_75_delta_365_day: float = Field(..., alias='exErnDlt75Iv1y')
    iv_95_delta_10_day: float = Field(..., alias='dlt95Iv10d')
    iv_95_delta_20_day: float = Field(..., alias='dlt95Iv20d')
    iv_95_delta_30_day: float = Field(..., alias='dlt95Iv30d')
    iv_95_delta_60_day: float = Field(..., alias='dlt95Iv60d')
    iv_95_delta_90_day: float = Field(..., alias='dlt95Iv90d')
    iv_95_delta_180_day: float = Field(..., alias='dlt95Iv6m')
    iv_95_delta_365_day: float = Field(..., alias='dlt95Iv1y')
    iv_ex_earnings_95_delta_10_day: float = Field(..., alias='exErnDlt95Iv10d')
    iv_ex_earnings_95_delta_20_day: float = Field(..., alias='exErnDlt95Iv20d')
    iv_ex_earnings_95_delta_30_day: float = Field(..., alias='exErnDlt95Iv30d')
    iv_ex_earnings_95_delta_60_day: float = Field(..., alias='exErnDlt95Iv60d')
    iv_ex_earnings_95_delta_90_day: float = Field(..., alias='exErnDlt95Iv90d')
    iv_ex_earnings_95_delta_180_day: float = Field(..., alias='exErnDlt95Iv6m')
    iv_ex_earnings_95_delta_365_day: float = Field(..., alias='exErnDlt95Iv1y')
    forward_volatility_30_20: float = Field(..., alias='fwd30_20')
    forward_volatility_60_30: float = Field(..., alias='fwd60_30')
    forward_volatility_90_60: float = Field(..., alias='fwd90_60')
    forward_volatility_180_90: float = Field(..., alias='fwd180_90')
    forward_volatility_90_30: float = Field(..., alias='fwd90_30')
    forward_ex_earnings_volatility_30_20: float = Field(..., alias='fexErn30_20')
    forward_ex_earnings_volatility_60_30: float = Field(..., alias='fexErn60_30')
    forward_ex_earnings_volatility_90_60: float = Field(..., alias='fexErn90_60')
    forward_ex_earnings_volatility_180_90: float = Field(..., alias='fexErn180_90')
    forward_ex_earnings_volatility_90_30: float = Field(..., alias='fexErn90_30')
    flat_forward_volatility_30_20: float = Field(..., alias='ffwd30_20')
    flat_forward_volatility_60_30: float = Field(..., alias='ffwd60_30')
    flat_forward_volatility_90_60: float = Field(..., alias='ffwd90_60')
    flat_forward_volatility_180_90: float = Field(..., alias='ffwd180_90')
    flat_forward_volatility_90_30: float = Field(..., alias='ffwd90_30')
    flat_forward_ex_earnings_volatility_30_20: float = Field(
        ..., alias='ffexErn30_20')
    flat_forward_ex_earnings_volatility_60_30: float = Field(
        ..., alias='ffexErn60_30')
    flat_forward_ex_earnings_volatility_90_60: float = Field(
        ..., alias='ffexErn90_60')
    flat_forward_ex_earnings_volatility_180_90: float = Field(
        ..., alias='ffexErn180_90')
    flat_forward_ex_earnings_volatility_90_30: float = Field(
        ..., alias='ffexErn90_30')
    forward_volatility_ratio_30_20: float = Field(..., alias='fbfwd30_20')
    forward_volatility_ratio_60_30: float = Field(..., alias='fbfwd60_30')
    forward_volatility_ratio_90_60: float = Field(..., alias='fbfwd90_60')
    forward_volatility_ratio_180_90: float = Field(..., alias='fbfwd180_90')
    forward_volatility_ratio_90_30: float = Field(..., alias='fbfwd90_30')
    forward_ex_earnings_volatility_ratio_30_20: float = Field(
        ..., alias='fbfexErn30_20')
    forward_ex_earnings_volatility_ratio_60_30: float = Field(
        ..., alias='fbfexErn60_30')
    forward_ex_earnings_volatility_ratio_90_60: float = Field(
        ..., alias='fbfexErn90_60')
    forward_ex_earnings_volatility_ratio_180_90: float = Field(
        ..., alias='fbfexErn180_90')
    forward_ex_earnings_volatility_ratio_90_30: float = Field(
        ..., alias='fbfexErn90_30')
    updated_at: datetime.datetime = Field(..., alias='updatedAt')
