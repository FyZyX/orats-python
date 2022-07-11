import datetime
import json
import os.path
import unittest
from unittest import skip

from orats.endpoints.data import DataApi
from orats.model.data import request as req
from orats.model.data import response as res


def test():
    path = os.path.join(os.path.dirname(__file__), "fixtures", "strike.json")
    with open(path) as handle:
        strike = res.StrikeResponse(**json.load(handle))
    print(strike)


class MyDataApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._api = DataApi("demo")

    def test_tickers(self):
        request = req.TickersRequest(ticker="IBM")
        tickers = self._api.tickers(request)
        self.assertEqual(len(tickers), 1)
        ticker = tickers[0]
        self.assertIsInstance(ticker, res.TickerResponse)
        self.assertIsInstance(ticker.underlying_symbol, str)
        self.assertIsInstance(ticker.max_date, datetime.date)
        self.assertIsInstance(ticker.min_date, datetime.date)

    def test_strikes(self):
        request = req.StrikesRequest(
            tickers=("IBM",),
            expiration_range=(30, ...),
            delta_range=(0.30, 0.45),
        )
        strikes = self._api.strikes(request)
        for strike in strikes:
            self.assertIsInstance(strike, res.StrikeResponse)

    @skip
    def test_strikes_history(self):
        request = req.StrikesHistoryRequest(
            tickers=("IBM", "AAPL"),
            trade_date=datetime.date(2022, 7, 5),
            expiration_range=(30, ...),
            delta_range=(0.30, 0.45),
        )
        strikes = self._api.strikes_history(request)
        for strike in strikes:
            self.assertIsInstance(strike, res.StrikeResponse)


if __name__ == "__main__":
    unittest.main()
