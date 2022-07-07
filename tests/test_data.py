import datetime
import json
import unittest

from orats.api.data import DataApi
from orats.model.strike import Strike
from orats.model.underlying import Ticker


def test():
    with open('../../tests/fixtures/strike.json') as handle:
        strike = Strike(**json.load(handle))
    print(strike)


class MyDataApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._api = DataApi('demo')

    def test_tickers(self):
        tickers = self._api.tickers('IBM')
        self.assertEqual(len(tickers), 1)
        ticker = tickers[0]
        self.assertIsInstance(ticker, Ticker)
        self.assertIsInstance(ticker.underlying_symbol, str)
        self.assertIsInstance(ticker.max_date, datetime.date)
        self.assertIsInstance(ticker.min_date, datetime.date)

    def test_strikes(self):
        strikes = self._api.strikes('IBM')
        for strike in strikes:
            self.assertIsInstance(strike, Strike)


if __name__ == '__main__':
    unittest.main()
