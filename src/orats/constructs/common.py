import os
from typing import Optional

from pydantic import BaseModel, Field


def _get_token() -> str:
    return os.environ.get("ORATS_API_TOKEN", "demo")


class Construct(BaseModel):
    _level: int
    _token: Optional[str] = Field(_get_token(), description="API token.")


class ApiConstruct(Construct):
    _level = 0


class IndustryConstruct(Construct):
    _level = 1


class ApplicationConstruct(Construct):
    _level = 2
