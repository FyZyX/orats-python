import os


def get_token() -> str:
    return os.environ.get("ORATS_API_TOKEN", "demo")
