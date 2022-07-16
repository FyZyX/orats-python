import os


def _get_token() -> str:
    return os.environ.get("ORATS_API_TOKEN", "demo")
