import json

from model import Strike


class DataApi:
    pass


if __name__ == '__main__':
    with open('fixtures/strike.json') as handle:
        strike = Strike(**json.load(handle))
    print(strike)
