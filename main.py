import json

from data import DataApi
from model import Strike


def entrypoint():
    api = DataApi('demo')
    print(api.tickers())


def test():
    with open('fixtures/strike.json') as handle:
        strike = Strike(**json.load(handle))
    print(strike)


if __name__ == '__main__':
    entrypoint()
