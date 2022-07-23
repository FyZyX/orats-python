import json
import os

from orats.sandbox.generator import fake_api_request


def persist_fixture(resource, fixture, prefix="data"):
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, "fixtures", prefix, f"{resource}.json")
    with open(path, "w") as file:
        json.dump(fixture, file, indent=2)


def _resource(url):
    return "/".join(url.split("://")[1].split("/")[2:])


def load_fixture(url, *args, **kwargs):
    return fake_api_request(_resource(url))
