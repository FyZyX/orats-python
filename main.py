import json

from model import Strike


class DataApi:
    pass


def entrypoint():
    with open('fixtures/strike.json') as handle:
        strike = Strike(**json.load(handle))
    print(strike)


if __name__ == '__main__':
    entrypoint()
