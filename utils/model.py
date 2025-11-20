from typing import Literal

from pydantic import BaseModel


class UserResponse(BaseModel):
    response: Literal["Accurate", "Inaccurate"]
    reasoning: str


class ReformulationQuery(BaseModel):
    text: str
