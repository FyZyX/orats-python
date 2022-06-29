import json

from data import DataApi
from model import Strike


def entrypoint():
    api = DataApi('demo')
    tickers = api.tickers('IBM')
    ticker = tickers[0]
    print(ticker.underlying_symbol)
    print(ticker.max_date - ticker.min_date)


def test():
    with open('../fixtures/strike.json') as handle:
        strike = Strike(**json.load(handle))
    print(strike)


if __name__ == '__main__':
    entrypoint()
