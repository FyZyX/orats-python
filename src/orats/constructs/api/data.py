import datetime
from typing import Optional

from pydantic import Field, validator

from orats.constructs.common import ApiConstruct


class DataApiConstruct(ApiConstruct):
    ticker: str = Field(..., alias="ticker")

    class Config:
        allow_population_by_field_name = True


class Ticker(DataApiConstruct):
    """Ticker symbol data duration definitions."""

    ticker: str = Field(..., alias="ticker")
    min_date: datetime.date = Field(..., alias="min")
    max_date: datetime.date = Field(..., alias="max")


class Strike(DataApiConstruct):
    """Verbose strike definitions.

    See corresponding `Strikes`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
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


class Money(DataApiConstruct):
    """Base class for impied and forecasted monies.

    This class helps abstract over the volatility surface construct.
    """

    ticker: str = Field(..., alias="ticker")
    trade_date: datetime.date = Field(..., alias="tradeDate")
    expiration_date: datetime.date = Field(..., alias="expirDate")
    underlying_price: float = Field(..., alias="stockPrice")
    risk_free_rate: float = Field(..., alias="riskFreeRate")
    iv_100_delta: float = Field(..., alias="vol100")
    iv_95_delta: float = Field(..., alias="vol95")
    iv_90_delta: float = Field(..., alias="vol90")
    iv_85_delta: float = Field(..., alias="vol85")
    iv_80_delta: float = Field(..., alias="vol80")
    iv_75_delta: float = Field(..., alias="vol75")
    iv_70_delta: float = Field(..., alias="vol70")
    iv_65_delta: float = Field(..., alias="vol65")
    iv_60_delta: float = Field(..., alias="vol60")
    iv_55_delta: float = Field(..., alias="vol55")
    iv_50_delta: float = Field(..., alias="vol50")
    iv_45_delta: float = Field(..., alias="vol45")
    iv_40_delta: float = Field(..., alias="vol40")
    iv_35_delta: float = Field(..., alias="vol35")
    iv_30_delta: float = Field(..., alias="vol30")
    iv_25_delta: float = Field(..., alias="vol25")
    iv_20_delta: float = Field(..., alias="vol20")
    iv_15_delta: float = Field(..., alias="vol15")
    iv_10_delta: float = Field(..., alias="vol10")
    iv_5_delta: float = Field(..., alias="vol5")
    iv_0_delta: float = Field(..., alias="vol0")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")


class MoneyImplied(Money):
    """Monthly implied money definitions.

    See corresponding `Monies Implied`_ response object.
    """

    spot_price: float = Field(..., alias="spotPrice")
    yield_rate: float = Field(..., alias="yieldRate")
    residual_yield_rate: float = Field(..., alias="residualYieldRate")
    residual_rate_slope: float = Field(..., alias="residualRateSlp")
    residual_r2: float = Field(..., alias="residualR2")
    confidence: float
    market_width: float = Field(..., alias="mwVol")
    atm_iv: float = Field(..., alias="atmiv")
    slope: float
    derivative: float = Field(..., alias="deriv")
    fit: float
    iv: float = Field(..., alias="calVol")
    unadjusted_iv: float = Field(..., alias="unadjVol")
    earnings_effect: float = Field(..., alias="earnEffect")


class MoneyForecast(Money):
    """Monthly forecast money definitions.

    See corresponding `Monies Forecast`_ response object.
    """


class Summary(DataApiConstruct):
    """SMV Summary data definitions.

    See corresponding `Summaries`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
    trade_date: datetime.date = Field(..., alias="tradeDate")
    underlying_price: float = Field(..., alias="stockPrice")
    annual_dividend: float = Field(..., alias="annActDiv")
    annual_implied_dividend: float = Field(..., alias="annIdiv")
    next_dividend: float = Field(..., alias="nextDiv")
    implied_next_dividend: float = Field(..., alias="impliedNextDiv")
    hard_to_borrow_30_days: float = Field(..., alias="borrow30")
    hard_to_borrow_2_years: float = Field(..., alias="borrow2y")
    confidence: float
    iv_ex_earnings_10_day: float = Field(..., alias="exErnIv10d")
    iv_ex_earnings_20_day: float = Field(..., alias="exErnIv20d")
    iv_ex_earnings_30_day: float = Field(..., alias="exErnIv30d")
    iv_ex_earnings_60_day: float = Field(..., alias="exErnIv60d")
    iv_ex_earnings_90_day: float = Field(..., alias="exErnIv90d")
    iv_ex_earnings_180_day: float = Field(..., alias="exErnIv6m")
    iv_ex_earnings_365_day: float = Field(..., alias="exErnIv1y")
    implied_earnings_effect: float = Field(..., alias="ieeEarnEffect")
    implied_move: float = Field(..., alias="impliedMove")
    implied_earnings_move: float = Field(..., alias="impliedEarningsMove")
    iv_interpolated_10_day: float = Field(..., alias="iv10d")
    iv_interpolated_20_day: float = Field(..., alias="iv20d")
    iv_interpolated_30_day: float = Field(..., alias="iv30d")
    iv_interpolated_60_day: float = Field(..., alias="iv60d")
    iv_interpolated_90_day: float = Field(..., alias="iv90d")
    iv_interpolated_180_day: float = Field(..., alias="iv6m")
    iv_interpolated_365_day: float = Field(..., alias="iv1y")
    market_width_30_day: float = Field(..., alias="mwAdj30")
    market_width_2_year: float = Field(..., alias="mwAdj2y")
    derivative_30_day: float = Field(..., alias="rDrv30")
    derivative_2_year: float = Field(..., alias="rDrv2y")
    slope_30_day: float = Field(..., alias="rSlp30")
    slope_2_year: float = Field(..., alias="rSlp2y")
    iv_30_day: float = Field(..., alias="rVol30")
    iv_2_year: float = Field(..., alias="rVol2y")
    ignore_price: float = Field(..., alias="rip")
    risk_free_rate_30_day: float = Field(..., alias="riskFree30")
    risk_free_rate_2_year: float = Field(..., alias="riskFree2y")
    skewing: float
    contango: float
    total_error_confidence: float = Field(..., alias="totalErrorConf")
    iv_5_delta_10_day: float = Field(..., alias="dlt5Iv10d")
    iv_5_delta_20_day: float = Field(..., alias="dlt5Iv20d")
    iv_5_delta_30_day: float = Field(..., alias="dlt5Iv30d")
    iv_5_delta_60_day: float = Field(..., alias="dlt5Iv60d")
    iv_5_delta_90_day: float = Field(..., alias="dlt5Iv90d")
    iv_5_delta_180_day: float = Field(..., alias="dlt5Iv6m")
    iv_5_delta_365_day: float = Field(..., alias="dlt5Iv1y")
    iv_ex_earnings_5_delta_10_day: float = Field(..., alias="exErnDlt5Iv10d")
    iv_ex_earnings_5_delta_20_day: float = Field(..., alias="exErnDlt5Iv20d")
    iv_ex_earnings_5_delta_30_day: float = Field(..., alias="exErnDlt5Iv30d")
    iv_ex_earnings_5_delta_60_day: float = Field(..., alias="exErnDlt5Iv60d")
    iv_ex_earnings_5_delta_90_day: float = Field(..., alias="exErnDlt5Iv90d")
    iv_ex_earnings_5_delta_180_day: float = Field(..., alias="exErnDlt5Iv6m")
    iv_ex_earnings_5_delta_365_day: float = Field(..., alias="exErnDlt5Iv1y")
    iv_25_delta_10_day: float = Field(..., alias="dlt25Iv10d")
    iv_25_delta_20_day: float = Field(..., alias="dlt25Iv20d")
    iv_25_delta_30_day: float = Field(..., alias="dlt25Iv30d")
    iv_25_delta_60_day: float = Field(..., alias="dlt25Iv60d")
    iv_25_delta_90_day: float = Field(..., alias="dlt25Iv90d")
    iv_25_delta_180_day: float = Field(..., alias="dlt25Iv6m")
    iv_25_delta_365_day: float = Field(..., alias="dlt25Iv1y")
    iv_ex_earnings_25_delta_10_day: float = Field(..., alias="exErnDlt25Iv10d")
    iv_ex_earnings_25_delta_20_day: float = Field(..., alias="exErnDlt25Iv20d")
    iv_ex_earnings_25_delta_30_day: float = Field(..., alias="exErnDlt25Iv30d")
    iv_ex_earnings_25_delta_60_day: float = Field(..., alias="exErnDlt25Iv60d")
    iv_ex_earnings_25_delta_90_day: float = Field(..., alias="exErnDlt25Iv90d")
    iv_ex_earnings_25_delta_180_day: float = Field(..., alias="exErnDlt25Iv6m")
    iv_ex_earnings_25_delta_365_day: float = Field(..., alias="exErnDlt25Iv1y")
    iv_75_delta_10_day: float = Field(..., alias="dlt75Iv10d")
    iv_75_delta_20_day: float = Field(..., alias="dlt75Iv20d")
    iv_75_delta_30_day: float = Field(..., alias="dlt75Iv30d")
    iv_75_delta_60_day: float = Field(..., alias="dlt75Iv60d")
    iv_75_delta_90_day: float = Field(..., alias="dlt75Iv90d")
    iv_75_delta_180_day: float = Field(..., alias="dlt75Iv6m")
    iv_75_delta_365_day: float = Field(..., alias="dlt75Iv1y")
    iv_ex_earnings_75_delta_10_day: float = Field(..., alias="exErnDlt75Iv10d")
    iv_ex_earnings_75_delta_20_day: float = Field(..., alias="exErnDlt75Iv20d")
    iv_ex_earnings_75_delta_30_day: float = Field(..., alias="exErnDlt75Iv30d")
    iv_ex_earnings_75_delta_60_day: float = Field(..., alias="exErnDlt75Iv60d")
    iv_ex_earnings_75_delta_90_day: float = Field(..., alias="exErnDlt75Iv90d")
    iv_ex_earnings_75_delta_180_day: float = Field(..., alias="exErnDlt75Iv6m")
    iv_ex_earnings_75_delta_365_day: float = Field(..., alias="exErnDlt75Iv1y")
    iv_95_delta_10_day: float = Field(..., alias="dlt95Iv10d")
    iv_95_delta_20_day: float = Field(..., alias="dlt95Iv20d")
    iv_95_delta_30_day: float = Field(..., alias="dlt95Iv30d")
    iv_95_delta_60_day: float = Field(..., alias="dlt95Iv60d")
    iv_95_delta_90_day: float = Field(..., alias="dlt95Iv90d")
    iv_95_delta_180_day: float = Field(..., alias="dlt95Iv6m")
    iv_95_delta_365_day: float = Field(..., alias="dlt95Iv1y")
    iv_ex_earnings_95_delta_10_day: float = Field(..., alias="exErnDlt95Iv10d")
    iv_ex_earnings_95_delta_20_day: float = Field(..., alias="exErnDlt95Iv20d")
    iv_ex_earnings_95_delta_30_day: float = Field(..., alias="exErnDlt95Iv30d")
    iv_ex_earnings_95_delta_60_day: float = Field(..., alias="exErnDlt95Iv60d")
    iv_ex_earnings_95_delta_90_day: float = Field(..., alias="exErnDlt95Iv90d")
    iv_ex_earnings_95_delta_180_day: float = Field(..., alias="exErnDlt95Iv6m")
    iv_ex_earnings_95_delta_365_day: float = Field(..., alias="exErnDlt95Iv1y")
    forward_volatility_30_20: float = Field(..., alias="fwd30_20")
    forward_volatility_60_30: float = Field(..., alias="fwd60_30")
    forward_volatility_90_60: float = Field(..., alias="fwd90_60")
    forward_volatility_180_90: float = Field(..., alias="fwd180_90")
    forward_volatility_90_30: float = Field(..., alias="fwd90_30")
    forward_ex_earnings_volatility_30_20: float = Field(..., alias="fexErn30_20")
    forward_ex_earnings_volatility_60_30: float = Field(..., alias="fexErn60_30")
    forward_ex_earnings_volatility_90_60: float = Field(..., alias="fexErn90_60")
    forward_ex_earnings_volatility_180_90: float = Field(..., alias="fexErn180_90")
    forward_ex_earnings_volatility_90_30: float = Field(..., alias="fexErn90_30")
    flat_forward_volatility_30_20: float = Field(..., alias="ffwd30_20")
    flat_forward_volatility_60_30: float = Field(..., alias="ffwd60_30")
    flat_forward_volatility_90_60: float = Field(..., alias="ffwd90_60")
    flat_forward_volatility_180_90: float = Field(..., alias="ffwd180_90")
    flat_forward_volatility_90_30: float = Field(..., alias="ffwd90_30")
    flat_forward_ex_earnings_volatility_30_20: float = Field(..., alias="ffexErn30_20")
    flat_forward_ex_earnings_volatility_60_30: float = Field(..., alias="ffexErn60_30")
    flat_forward_ex_earnings_volatility_90_60: float = Field(..., alias="ffexErn90_60")
    flat_forward_ex_earnings_volatility_180_90: float = Field(
        ..., alias="ffexErn180_90"
    )
    flat_forward_ex_earnings_volatility_90_30: float = Field(..., alias="ffexErn90_30")
    forward_volatility_ratio_30_20: float = Field(..., alias="fbfwd30_20")
    forward_volatility_ratio_60_30: float = Field(..., alias="fbfwd60_30")
    forward_volatility_ratio_90_60: float = Field(..., alias="fbfwd90_60")
    forward_volatility_ratio_180_90: float = Field(..., alias="fbfwd180_90")
    forward_volatility_ratio_90_30: float = Field(..., alias="fbfwd90_30")
    forward_ex_earnings_volatility_ratio_30_20: float = Field(
        ..., alias="fbfexErn30_20"
    )
    forward_ex_earnings_volatility_ratio_60_30: float = Field(
        ..., alias="fbfexErn60_30"
    )
    forward_ex_earnings_volatility_ratio_90_60: float = Field(
        ..., alias="fbfexErn90_60"
    )
    forward_ex_earnings_volatility_ratio_180_90: float = Field(
        ..., alias="fbfexErn180_90"
    )
    forward_ex_earnings_volatility_ratio_90_30: float = Field(
        ..., alias="fbfexErn90_30"
    )
    updated_at: datetime.datetime = Field(..., alias="updatedAt")


class Core(DataApiConstruct):
    """Core definitions.

    See corresponding `Core`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
    trade_date: datetime.date = Field(..., alias="tradeDate")
    asset_type: int = Field(..., alias="assetType")
    prior_close: float = Field(..., alias="priorCls")
    underlying_price_atm: float = Field(..., alias="pxAtmIv")
    market_capitalization: int = Field(..., alias="mktCap")
    call_volume: int = Field(..., alias="cVolu")
    call_open_interest: int = Field(..., alias="cOi")
    put_volume: int = Field(..., alias="pVolu")
    put_open_interest: int = Field(..., alias="pOi")
    underlying_volatility_forecast: float = Field(..., alias="orFcst20d")
    iv_forecast: float = Field(..., alias="orIvFcst20d")
    iv_infinite_forecast: float = Field(..., alias="orFcstInf")
    iv_ex_earnings_20_day: float = Field(..., alias="orIvXern20d")
    iv_ex_earnings_infinite: float = Field(..., alias="orIvXernInf")
    iv_ex_earnings_20_day_200ma: float = Field(..., alias="iv200Ma")
    iv_atm_1_month: float = Field(..., alias="atmIvM1")
    fit_atm_1_month: float = Field(..., alias="atmFitIvM1")
    iv_atm_forecast_1_month: float = Field(..., alias="atmFcstIvM1")
    days_to_expiration_1_month: int = Field(..., alias="dtExM1")
    iv_atm_2_month: float = Field(..., alias="atmIvM2")
    fit_atm_2_month: float = Field(..., alias="atmFitIvM2")
    iv_atm_forecast_2_month: float = Field(..., alias="atmFcstIvM2")
    days_to_expiration_2_month: int = Field(..., alias="dtExM2")
    iv_atm_3_month: float = Field(..., alias="atmIvM3")
    fit_atm_3_month: float = Field(..., alias="atmFitIvM3")
    iv_atm_forecast_3_month: float = Field(..., alias="atmFcstIvM3")
    days_to_expiration_3_month: int = Field(..., alias="dtExM3")
    iv_atm_4_month: float = Field(..., alias="atmIvM4")
    fit_atm_4_month: float = Field(..., alias="atmFitIvM4")
    iv_atm_forecast_4_month: float = Field(..., alias="atmFcstIvM4")
    days_to_expiration_4_month: int = Field(..., alias="dtExM4")
    risk_free_rate_5_week: float = Field(..., alias="iRate5wk")
    risk_free_rate: float = Field(..., alias="iRateLt")
    price_1k_gamma: float = Field(..., alias="px1kGam")
    volatility_of_volatility: float = Field(..., alias="volOfVol")
    volatility_of_iv: float = Field(..., alias="volOfIvol")
    slope: float
    implied_infinite_slope: float = Field(..., alias="slopeInf")
    slope_forecast: float = Field(..., alias="slopeFcst")
    implied_infinite_slope_forecast: float = Field(..., alias="slopeFcstInf")
    derivative: float = Field(..., alias="deriv")
    implied_infinite_derivative: float = Field(..., alias="derivInf")
    derivative_forecast: float = Field(..., alias="derivFcst")
    implied_infinite_derivative_forecast: float = Field(..., alias="derivFcstInf")
    market_width: float = Field(..., alias="mktWidthVol")
    implied_infinite_market_width: float = Field(..., alias="mktWidthVolInf")
    ignore_price: float = Field(..., alias="rip")
    iv_earnings_return: float = Field(..., alias="ivEarnReturn")
    volatility_goodness_of_fit: float = Field(..., alias="fcstR2")
    iv_goodness_of_fit: float = Field(..., alias="fcstR2Imp")
    total_stock_volume: int = Field(..., alias="stkVolu")
    average_option_volume_20_day: float = Field(..., alias="avgOptVolu20d")
    sector: str
    hv_1_day: float = Field(..., alias="orHv1d")
    hv_5_day: float = Field(..., alias="orHv5d")
    hv_10_day: float = Field(..., alias="orHv10d")
    hv_20_day: float = Field(..., alias="orHv20d")
    hv_60_day: float = Field(..., alias="orHv60d")
    hv_90_day: float = Field(..., alias="orHv90d")
    hv_120_day: float = Field(..., alias="orHv120d")
    hv_252_day: float = Field(..., alias="orHv252d")
    hv_500_day: float = Field(..., alias="orHv500d")
    hv_1000_day: float = Field(..., alias="orHv1000d")
    close_to_close_hv_5_day: float = Field(..., alias="clsHv5d")
    close_to_close_hv_10_day: float = Field(..., alias="clsHv10d")
    close_to_close_hv_20_day: float = Field(..., alias="clsHv20d")
    close_to_close_hv_60_day: float = Field(..., alias="clsHv60d")
    close_to_close_hv_90_day: float = Field(..., alias="clsHv90d")
    close_to_close_hv_120_day: float = Field(..., alias="clsHv120d")
    close_to_close_hv_252_day: float = Field(..., alias="clsHv252d")
    close_to_close_hv_500_day: float = Field(..., alias="clsHv500d")
    close_to_close_hv_1000_day: float = Field(..., alias="clsHv1000d")
    underlying_close_prior_week: float = Field(..., alias="clsPx1w")
    underlying_change_prior_week: float = Field(..., alias="stkPxChng1wk")
    underlying_close_prior_month: float = Field(..., alias="clsPx1m")
    underlying_change_prior_month: float = Field(..., alias="stkPxChng1m")
    underlying_close_prior_6_months: float = Field(..., alias="clsPx6m")
    underlying_change_prior_6_months: float = Field(..., alias="stkPxChng6m")
    underlying_close_prior_year: float = Field(..., alias="clsPx1y")
    underlying_change_prior_year: float = Field(..., alias="stkPxChng1y")
    dividend_frequency: int = Field(..., alias="divFreq")
    dividend_yield: float = Field(..., alias="divYield")
    dividend_growth: float = Field(..., alias="divGrwth")
    next_dividend_date: datetime.date = Field(..., alias="divDate")
    dividend_amount: float = Field(..., alias="divAmt")
    next_earnings_date: Optional[datetime.date] = Field(..., alias="nextErn")
    last_earnings_date: datetime.date = Field(..., alias="lastErn")
    last_earnings_time_of_day: int = Field(..., alias="lastErnTod")
    average_earnings_move: float = Field(..., alias="absAvgErnMv")
    market_implied_earnings_effect: float = Field(..., alias="impliedIee")
    takeover: bool = Field(..., alias="tkOver")
    etfs: str = Field(..., alias="etfIncl")
    best_etf: str = Field(..., alias="bestEtf")
    sector_name: str = Field(..., alias="sectorName")
    correlation_to_spy_1_month: float = Field(..., alias="correlSpy1m")
    correlation_to_spy_1_year: float = Field(..., alias="correlSpy1y")
    correlation_to_best_etf_1_month: float = Field(..., alias="correlEtf1m")
    correlation_to_best_etf_1_year: float = Field(..., alias="correlEtf1y")
    beta_1_month: float = Field(..., alias="beta1m")
    beta_1_year: float = Field(..., alias="beta1y")
    iv_percentile_1_month: int = Field(..., alias="ivPctile1m")
    iv_percentile_1_year: int = Field(..., alias="ivPctile1y")
    iv_percentile_spy: int = Field(..., alias="ivPctileSpy")
    iv_percentile_etf: int = Field(..., alias="ivPctileEtf")
    iv_standard_deviations_from_mean: float = Field(..., alias="ivStdvMean")
    iv_standard_deviation_1_year: float = Field(..., alias="ivStdv1y")
    iv_spy_ratio: float = Field(..., alias="ivSpyRatio")
    iv_spy_ratio_average_1_month: float = Field(..., alias="ivSpyRatioAvg1m")
    iv_spy_ratio_average_1_year: float = Field(..., alias="ivSpyRatioAvg1y")
    iv_spy_ratio_standard_deviation_1_year: float = Field(..., alias="ivSpyRatioStdv1y")
    iv_etf_ratio: float = Field(..., alias="ivEtfRatio")
    iv_etf_ratio_average_1_month: float = Field(..., alias="ivEtfRatioAvg1m")
    iv_etf_ratio_average_1_year: float = Field(..., alias="ivEtfRatioAvg1y")
    iv_etf_ratio_standard_deviation_1_year: float = Field(..., alias="ivEtFratioStdv1y")
    iv_hv_ex_earnings_ratio: float = Field(..., alias="ivHvXernRatio")
    iv_hv_ex_earnings_ratio_average_1_month: float = Field(..., alias="ivHvXernRatio1m")
    iv_hv_ex_earnings_ratio_average_1_year: float = Field(..., alias="ivHvXernRatio1y")
    iv_hv_ex_earnings_ratio_standard_deviation_1_year: float = Field(
        ..., alias="ivHvXernRatioStdv1y"
    )
    etf_iv_hv_ex_earnings_ratio: float = Field(..., alias="etfIvHvXernRatio")
    etf_iv_hv_ex_earnings_ratio_average_1_month: float = Field(
        ..., alias="etfIvHvXernRatio1m"
    )
    etf_iv_hv_ex_earnings_ratio_average_1_year: float = Field(
        ..., alias="etfIvHvXernRatio1y"
    )
    etf_iv_hv_ex_earnings_ratio_standard_deviation_1_year: float = Field(
        ..., alias="etfIvHvXernRatioStdv1y"
    )
    slope_percentile: float = Field(..., alias="slopepctile")
    slope_average_1_month: float = Field(..., alias="slopeavg1m")
    slope_average_1_year: float = Field(..., alias="slopeavg1y")
    slope_standard_deviation_1_year: float = Field(..., alias="slopeStdv1y")
    etf_slope_ex_earnings_ratio: float = Field(..., alias="etfSlopeRatio")
    etf_slope_ex_earnings_ratio_average_1_month: float = Field(
        ..., alias="etfSlopeRatioAvg1m"
    )
    etf_slope_ex_earnings_ratio_average_1_year: float = Field(
        ..., alias="etfSlopeRatioAvg1y"
    )
    etf_slope_ex_earnings_ratio_standard_deviation_1_year: float = Field(
        ..., alias="etfSlopeRatioAvgStdv1y"
    )
    implied_goodness_of_fit: float = Field(..., alias="impliedR2")
    contango: float
    next_dividend: float = Field(..., alias="nextDiv")
    implied_next_dividend: float = Field(..., alias="impliedNextDiv")
    annual_expected_dividend: float = Field(..., alias="annActDiv")
    annual_implied_dividend: float = Field(..., alias="annIdiv")
    hard_to_borrow_30_days: float = Field(..., alias="borrow30")
    hard_to_borrow_2_years: float = Field(..., alias="borrow2yr")
    error: float
    confidence: float
    underlying_close: float = Field(..., alias="pxCls")
    weeks_to_next_earnings: int = Field(..., alias="wksNextErn")
    option_volume_average_20_days: float = Field(..., alias="avgOptVolu20d")
    open_interest: int = Field(..., alias="oi")
    straddle_price_1_month: float = Field(..., alias="straPxM1")
    straddle_price_2_month: float = Field(..., alias="straPxM2")
    straddle_smooth_price_1_month: float = Field(..., alias="smoothStraPxM1")
    straddle_smooth_price_2_month: float = Field(..., alias="smoothStrPxM2")
    straddle_forecast_price_1_month: float = Field(..., alias="fcstStraPxM1")
    straddle_forecast_price_2_month: float = Field(..., alias="fcstStraPxM2")
    low_strike_1_month: int = Field(..., alias="loStrikeM1")
    high_strike_1_month: int = Field(..., alias="hiStrikeM1")
    low_strike_2_month: int = Field(..., alias="loStrikeM2")
    high_strike_2_month: int = Field(..., alias="hiStrikeM2")
    earnings_date_1: datetime.date = Field(..., alias="ernDate1")
    earnings_date_2: datetime.date = Field(..., alias="ernDate2")
    earnings_date_3: datetime.date = Field(..., alias="ernDate3")
    earnings_date_4: datetime.date = Field(..., alias="ernDate4")
    earnings_date_5: datetime.date = Field(..., alias="ernDate5")
    earnings_date_6: datetime.date = Field(..., alias="ernDate6")
    earnings_date_7: datetime.date = Field(..., alias="ernDate7")
    earnings_date_8: datetime.date = Field(..., alias="ernDate8")
    earnings_date_9: datetime.date = Field(..., alias="ernDate9")
    earnings_date_10: datetime.date = Field(..., alias="ernDate10")
    earnings_date_11: datetime.date = Field(..., alias="ernDate11")
    earnings_date_12: datetime.date = Field(..., alias="ernDate12")
    earnings_move_1: float = Field(..., alias="ernMv1")
    earnings_move_2: float = Field(..., alias="ernMv2")
    earnings_move_3: float = Field(..., alias="ernMv3")
    earnings_move_4: float = Field(..., alias="ernMv4")
    earnings_move_5: float = Field(..., alias="ernMv5")
    earnings_move_6: float = Field(..., alias="ernMv6")
    earnings_move_7: float = Field(..., alias="ernMv7")
    earnings_move_8: float = Field(..., alias="ernMv8")
    earnings_move_9: float = Field(..., alias="ernMv9")
    earnings_move_10: float = Field(..., alias="ernMv10")
    earnings_move_11: float = Field(..., alias="ernMv11")
    earnings_move_12: float = Field(..., alias="ernMv12")
    earnings_straddle_percent_1: float = Field(..., alias="ernStraPct1")
    earnings_straddle_percent_2: float = Field(..., alias="ernStraPct2")
    earnings_straddle_percent_3: float = Field(..., alias="ernStraPct3")
    earnings_straddle_percent_4: float = Field(..., alias="ernStraPct4")
    earnings_straddle_percent_5: float = Field(..., alias="ernStraPct5")
    earnings_straddle_percent_6: float = Field(..., alias="ernStraPct6")
    earnings_straddle_percent_7: float = Field(..., alias="ernStraPct7")
    earnings_straddle_percent_8: float = Field(..., alias="ernStraPct8")
    earnings_straddle_percent_9: float = Field(..., alias="ernStraPct9")
    earnings_straddle_percent_10: float = Field(..., alias="ernStraPct10")
    earnings_straddle_percent_11: float = Field(..., alias="ernStraPct11")
    earnings_straddle_percent_12: float = Field(..., alias="ernStraPct12")
    earnings_effect_1: float = Field(..., alias="ernEffct1")
    earnings_effect_2: float = Field(..., alias="ernEffct2")
    earnings_effect_3: float = Field(..., alias="ernEffct3")
    earnings_effect_4: float = Field(..., alias="ernEffct4")
    earnings_effect_5: float = Field(..., alias="ernEffct5")
    earnings_effect_6: float = Field(..., alias="ernEffct6")
    earnings_effect_7: float = Field(..., alias="ernEffct7")
    earnings_effect_8: float = Field(..., alias="ernEffct8")
    earnings_effect_9: float = Field(..., alias="ernEffct9")
    earnings_effect_10: float = Field(..., alias="ernEffct10")
    earnings_effect_11: float = Field(..., alias="ernEffct11")
    earnings_effect_12: float = Field(..., alias="ernEffct12")
    hv_ex_earnings_5_day: float = Field(..., alias="orHvXern5d")
    hv_ex_earnings_10_day: float = Field(..., alias="orHvXern10d")
    hv_ex_earnings_20_day: float = Field(..., alias="orHvXern20d")
    hv_ex_earnings_60_day: float = Field(..., alias="orHvXern60d")
    hv_ex_earnings_90_day: float = Field(..., alias="orHvXern90d")
    hv_ex_earnings_120_day: float = Field(..., alias="orHvXern120d")
    hv_ex_earnings_252_day: float = Field(..., alias="orHvXern252d")
    hv_ex_earnings_500_day: float = Field(..., alias="orHvXern500d")
    hv_ex_earnings_1000_day: float = Field(..., alias="orHvXern1000d")
    close_to_close_hv_ex_earnings_5_day: float = Field(..., alias="clsHvXern5d")
    close_to_close_hv_ex_earnings_10_day: float = Field(..., alias="clsHvXern10d")
    close_to_close_hv_ex_earnings_20_day: float = Field(..., alias="clsHvXern20d")
    close_to_close_hv_ex_earnings_60_day: float = Field(..., alias="clsHvXern60d")
    close_to_close_hv_ex_earnings_90_day: float = Field(..., alias="clsHvXern90d")
    close_to_close_hv_ex_earnings_120_day: float = Field(..., alias="clsHvXern120d")
    close_to_close_hv_ex_earnings_252_day: float = Field(..., alias="clsHvXern252d")
    close_to_close_hv_ex_earnings_500_day: float = Field(..., alias="clsHvXern500d")
    close_to_close_hv_ex_earnings_1000_day: float = Field(..., alias="clsHvXern1000d")
    iv_interpolated_10_day: float = Field(..., alias="iv10d")
    iv_interpolated_20_day: float = Field(..., alias="iv20d")
    iv_interpolated_30_day: float = Field(..., alias="iv30d")
    iv_interpolated_60_day: float = Field(..., alias="iv60d")
    iv_interpolated_90_day: float = Field(..., alias="iv90d")
    iv_interpolated_180_day: float = Field(..., alias="iv6m")
    iv_interpolated_365_day: float = Field(..., alias="iv1yr")
    # put_call_slope: float = Field(..., alias='slope')
    put_call_slope_forecast: float = Field(..., alias="fcstSlope")
    earnings_effect_forecast: float = Field(..., alias="fcstErnEffct")
    earnings_move_standard_deviation: float = Field(..., alias="ernMvStdv")
    implied_earnings_effect: float = Field(..., alias="impliedEe")
    implied_earnings_move: float = Field(..., alias="impErnMv")
    underlying_move_in_earnings_effect: float = Field(..., alias="impMth2ErnMv")
    iv_fair: float = Field(..., alias="fairVol90d")
    iv_ex_earnings_fair: float = Field(..., alias="fairXieeVol90d")
    iv_ex_earnings_interpolated_fair: float = Field(..., alias="fairMth2XieeVol90d")
    additional_implied_earnings_move_front_month: float = Field(
        ..., alias="impErnMv90d"
    )
    additional_implied_earnings_move_second_month: float = Field(
        ..., alias="impErnMvMth290d"
    )
    iv_ex_earnings_interpolated_10_day: float = Field(..., alias="exErnIv10d")
    iv_ex_earnings_interpolated_20_day: float = Field(..., alias="exErnIv20d")
    iv_ex_earnings_interpolated_30_day: float = Field(..., alias="exErnIv30d")
    iv_ex_earnings_interpolated_60_day: float = Field(..., alias="exErnIv60d")
    iv_ex_earnings_interpolated_90_day: float = Field(..., alias="exErnIv90d")
    iv_ex_earnings_interpolated_180_day: float = Field(..., alias="exErnIv6m")
    iv_ex_earnings_interpolated_365_day: float = Field(..., alias="exErnIv1yr")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")

    @validator(
        "earnings_date_1",
        "earnings_date_2",
        "earnings_date_3",
        "earnings_date_4",
        "earnings_date_5",
        "earnings_date_6",
        "earnings_date_7",
        "earnings_date_8",
        "earnings_date_9",
        "earnings_date_10",
        "earnings_date_11",
        "earnings_date_12",
        pre=True,
    )
    def normalize_dates(cls, value):
        return datetime.datetime.strptime(value, "%m/%d/%Y").date()

    @validator("next_earnings_date", pre=True)
    def ensure_valid_date(cls, value):
        if value == "0000-00-00":
            return None
        return value


class DailyPrice(DataApiConstruct):
    """Daily price definitions.

    See corresponding `Daily Price`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
    trade_date: datetime.date = Field(..., alias="tradeDate")
    open: float = Field(..., alias="open")
    high: float = Field(..., alias="hiPx")
    low: float = Field(..., alias="loPx")
    close: float = Field(..., alias="clsPx")
    volume: int = Field(..., alias="stockVolume")
    unadjusted_open: float = Field(..., alias="unadjOpen")
    unadjusted_high: float = Field(..., alias="unadjHiPx")
    unadjusted_low: float = Field(..., alias="unadjLoPx")
    unadjusted_close: float = Field(..., alias="unadjClsPx")
    unadjusted_volume: int = Field(..., alias="unadjStockVolume")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")


class HistoricalVolatility(DataApiConstruct):
    """Historical volatility definitions.

    See corresponding `Historical Volatility`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
    trade_date: datetime.date = Field(..., alias="tradeDate")
    hv_1_day: float = Field(..., alias="orHv1d")
    hv_5_day: float = Field(..., alias="orHv5d")
    hv_10_day: float = Field(..., alias="orHv10d")
    hv_20_day: float = Field(..., alias="orHv20d")
    hv_30_day: float = Field(..., alias="orHv30d")
    hv_60_day: float = Field(..., alias="orHv60d")
    hv_90_day: float = Field(..., alias="orHv90d")
    hv_100_day: float = Field(..., alias="orHv100d")
    hv_120_day: float = Field(..., alias="orHv120d")
    hv_252_day: float = Field(..., alias="orHv252d")
    hv_500_day: float = Field(..., alias="orHv500d")
    hv_1000_day: float = Field(..., alias="orHv1000d")
    close_to_close_hv_5_day: float = Field(..., alias="clsHv5d")
    close_to_close_hv_10_day: float = Field(..., alias="clsHv10d")
    close_to_close_hv_20_day: float = Field(..., alias="clsHv20d")
    close_to_close_hv_30_day: float = Field(..., alias="clsHv30d")
    close_to_close_hv_60_day: float = Field(..., alias="clsHv60d")
    close_to_close_hv_90_day: float = Field(..., alias="clsHv90d")
    close_to_close_hv_100_day: float = Field(..., alias="clsHv100d")
    close_to_close_hv_120_day: float = Field(..., alias="clsHv120d")
    close_to_close_hv_252_day: float = Field(..., alias="clsHv252d")
    close_to_close_hv_500_day: float = Field(..., alias="clsHv500d")
    close_to_close_hv_1000_day: float = Field(..., alias="clsHv1000d")
    hv_ex_earnings_5_day: float = Field(..., alias="orHvXern5d")
    hv_ex_earnings_10_day: float = Field(..., alias="orHvXern10d")
    hv_ex_earnings_20_day: float = Field(..., alias="orHvXern20d")
    hv_ex_earnings_30_day: float = Field(..., alias="orHvXern30d")
    hv_ex_earnings_60_day: float = Field(..., alias="orHvXern60d")
    hv_ex_earnings_90_day: float = Field(..., alias="orHvXern90d")
    hv_ex_earnings_100_day: float = Field(..., alias="orHvXern100d")
    hv_ex_earnings_120_day: float = Field(..., alias="orHvXern120d")
    hv_ex_earnings_252_day: float = Field(..., alias="orHvXern252d")
    hv_ex_earnings_500_day: float = Field(..., alias="orHvXern500d")
    hv_ex_earnings_1000_day: float = Field(..., alias="orHvXern1000d")
    close_to_close_hv_ex_earnings_5_day: float = Field(..., alias="clsHvXern5d")
    close_to_close_hv_ex_earnings_10_day: float = Field(..., alias="clsHvXern10d")
    close_to_close_hv_ex_earnings_20_day: float = Field(..., alias="clsHvXern20d")
    close_to_close_hv_ex_earnings_30_day: float = Field(..., alias="clsHvXern30d")
    close_to_close_hv_ex_earnings_60_day: float = Field(..., alias="clsHvXern60d")
    close_to_close_hv_ex_earnings_90_day: float = Field(..., alias="clsHvXern90d")
    close_to_close_hv_ex_earnings_100_day: float = Field(..., alias="clsHvXern100d")
    close_to_close_hv_ex_earnings_120_day: float = Field(..., alias="clsHvXern120d")
    close_to_close_hv_ex_earnings_252_day: float = Field(..., alias="clsHvXern252d")
    close_to_close_hv_ex_earnings_500_day: float = Field(..., alias="clsHvXern500d")
    close_to_close_hv_ex_earnings_1000_day: float = Field(..., alias="clsHvXern1000d")


class DividendHistory(DataApiConstruct):
    """Dividend History definitions.

    See corresponding `Dividend History`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
    ex_dividend_date: datetime.date = Field(..., alias="exDate")
    dividend_amount: float = Field(..., alias="divAmt")
    dividend_frequency: int = Field(..., alias="divFreq")
    declared_date: datetime.date = Field(..., alias="declaredDate")


class EarningsHistory(DataApiConstruct):
    """Earnings history definitions.

    See corresponding `Earnings History`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
    earnings_date: datetime.date = Field(..., alias="earnDate")
    time_of_day_announced: int = Field(..., alias="anncTod")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")


class StockSplitHistory(DataApiConstruct):
    """Stock split history definitions.

    See corresponding `Stock Split History`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
    split_date: datetime.date = Field(..., alias="splitDate")
    divisor: float


class IvRank(DataApiConstruct):
    """IV Rank definitions.

    See corresponding `IV Rank`_ response object.
    """

    ticker: str = Field(..., alias="ticker")
    trade_date: datetime.date = Field(..., alias="tradeDate")
    iv: float = Field(..., alias="iv")
    iv_rank_1_month: float = Field(..., alias="ivRank1m")
    iv_percentile_1_month: float = Field(..., alias="ivPct1m")
    iv_rank_1_year: float = Field(..., alias="ivRank1y")
    iv_percentile_1_year: float = Field(..., alias="ivPct1y")
    updated_at: datetime.datetime = Field(..., alias="updatedAt")
