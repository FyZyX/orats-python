from orats.sandbox.api.generator import FakeDataGenerator

_data_generator = FakeDataGenerator()
_data_definitions = {
    "tickers": _data_generator.ticker,
    "strikes": _data_generator.strike,
    "hist/strikes": _data_generator.strike,
    "strikes/options": _data_generator.strike,
    "hist/strikes/options": _data_generator.strike,
    "monies/implied": _data_generator.money_implied,
    "monies/forecast": _data_generator.money_forecast,
    "hist/monies/implied": _data_generator.money_implied,
    "hist/monies/forecast": _data_generator.money_forecast,
    "summaries": _data_generator.summary,
    "hist/summaries": _data_generator.summary,
    "cores": _data_generator.core,
    "hist/cores": _data_generator.core,
    "hist/dailies": _data_generator.daily_price,
    "hist/hvs": _data_generator.historical_volatility,
    "hist/divs": _data_generator.dividend_history,
    "hist/earnings": _data_generator.earnings_history,
    "hist/splits": _data_generator.stock_split_history,
    "ivrank": _data_generator.iv_rank,
    "hist/ivrank": _data_generator.iv_rank,
}


def _resource(url):
    return "/".join(url.split("://")[1].split("/")[2:])


def fake_api_response(url, params=None, body=None, count=1):
    data_definition = _data_definitions[_resource(url)]
    return {"data": [data_definition() for _ in range(count)]}
