from pydantic import BaseModel, Field


class OratsResponse(BaseModel):
    underlying_symbol: str = Field(..., alias="ticker")
