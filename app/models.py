from pydantic import BaseModel


class Query(BaseModel):
    prompt: str


class NormalResponse(BaseModel):
    reasoning: str
    answer: str


class ErrorResponse(BaseModel):
    message: str
