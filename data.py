import httpx


class DataApi:
    _base_url = 'https://api.orats.io/datav2'

    def __init__(self, token):
        self._token = token

    def _url(self, path):
        return '/'.join((self._base_url, path))

    def _update_params(self, params):
        updated_params = dict(token=self._token)
        for key, param in params:
            if param is None:
                continue
            updated_params[key] = param
        return updated_params

    def _get(self, path, **params):
        response = httpx.get(self._url(path), params=self._update_params(params))
        return response.json()

    def tickers(self, symbol=None):
        return self._get('tickers', ticker=symbol)

    def strikes(self, *symbols, fields=None, days_to_expiration=None, delta=None):
        return self._get(
            'strikes',
            ticker=','.join(symbols),
            fields=fields,
            dte=days_to_expiration,
            delta=delta,
        )

    def strikes_history(self, *symbols, trade_date, fields=None,
                        days_to_expiration=None, delta=None):
        return self._get(
            'hist/strikes',
            ticker=','.join(symbols),
            tradeDate=trade_date,
            fields=fields,
            dte=days_to_expiration,
            delta=delta,
        )

    def strikes_by_options(self, symbol, expiration_date, strike):
        return self._get(
            'strikes/options',
            ticker=symbol,
            expirDate=expiration_date,
            strike=strike,
        )

    def strikes_history_by_options(self, symbol, expiration_date, strike,
                                   trade_date=None):
        return self._get(
            'hist/strikes/options',
            ticker=symbol,
            tradeDate=trade_date,
            expirDate=expiration_date,
            strike=strike,
        )

    def monies_implied(self, *symbols, fields=None):
        return self._get(
            'monies/implied',
            ticker=','.join(symbols),
            fields=fields,
        )

    def monies_forecast(self, *symbols, fields=None):
        return self._get(
            'monies/forecast',
            ticker=','.join(symbols),
            fields=fields,
        )

    def monies_implied_history(self, *symbols, trade_date, fields=None):
        return self._get(
            'hist/monies/implied',
            ticker=','.join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )

    def monies_forecast_history(self, *symbols, trade_date, fields=None):
        return self._get(
            'hist/monies/forecast',
            ticker=','.join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )

    def summaries(self, *symbols, fields=None):
        return self._get(
            'summaries',
            ticker=','.join(symbols),
            fields=fields,
        )

    def summaries_history(self, *symbols, trade_date=None, fields=None):
        assert len(symbols) and trade_date is not None
        return self._get(
            'hist/summaries',
            ticker=','.join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )

    def core_data(self, *symbols, fields=None):
        return self._get(
            'cores',
            ticker=','.join(symbols),
            fields=fields,
        )

    def core_data_history(self, *symbols, trade_date=None, fields=None):
        assert len(symbols) and trade_date is not None
        return self._get(
            'hist/cores',
            ticker=','.join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )

    def daily_price(self, *symbols, trade_date=None, fields=None):
        assert len(symbols) and trade_date is not None
        return self._get(
            'hist/dailies',
            ticker=','.join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )

    def historical_volatility(self, *symbols, trade_date=None, fields=None):
        assert len(symbols) and trade_date is not None
        return self._get(
            'hist/hvs',
            ticker=','.join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )

    def dividend_history(self, *symbols):
        return self._get(
            'hist/divs',
            ticker=','.join(symbols),
        )

    def stock_split_history(self, *symbols):
        return self._get(
            'hist/splits',
            ticker=','.join(symbols),
        )

    def iv_rank(self, *symbols, fields=None):
        return self._get(
            'ivrank',
            ticker=','.join(symbols),
            fields=fields,
        )

    def iv_rank_history(self, *symbols, trade_date=None, fields=None):
        assert len(symbols) and trade_date is not None
        return self._get(
            'hist/ivrank',
            ticker=','.join(symbols),
            tradeDate=trade_date,
            fields=fields,
        )
