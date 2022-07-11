from pydantic import BaseModel, Field


class DataApiResponse(BaseModel):
    underlying_symbol: str = Field(..., alias="ticker")
