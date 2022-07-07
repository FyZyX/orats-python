from orats.api.data import DataApi


def entrypoint():
    api = DataApi("demo")
    tickers = api.tickers("IBM")
    ticker = tickers[0]
    print(ticker.underlying_symbol)
    print(ticker.max_date - ticker.min_date)


if __name__ == "__main__":
    entrypoint()
