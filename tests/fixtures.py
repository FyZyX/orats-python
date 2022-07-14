import json
import os


def persist_fixture(endpoint, fixture, prefix="data"):
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, "fixtures", prefix, f"{endpoint}.json")
    with open(path, "w") as file:
        json.dump(fixture, file, indent=2)


def load_fixture(self, request):
    directory = os.path.dirname(__file__)
    key = self._resource.replace("/", "-")
    path = os.path.join(directory, "fixtures", "data", f"{key}.json")
    with open(path) as file:
        return json.load(file)["data"]
