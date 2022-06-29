import datetime
import unittest

from src import model
from src.data import DataApi


class MyDataApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._api = DataApi('demo')

    def test_tickers(self):
        tickers = self._api.tickers('IBM')
        self.assertEqual(len(tickers), 1)
        ticker = tickers[0]
        self.assertIsInstance(ticker, model.Ticker)
        self.assertIsInstance(ticker.underlying_symbol, str)
        self.assertIsInstance(ticker.max_date, datetime.date)
        self.assertIsInstance(ticker.min_date, datetime.date)

    def test_strikes(self):
        strikes = self._api.strikes('IBM')
        for strike in strikes:
            self.assertIsInstance(strike, model.Strike)


if __name__ == '__main__':
    unittest.main()
