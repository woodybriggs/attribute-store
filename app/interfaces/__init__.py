from ..db import Base
from pydantic import BaseModel, StrictBool, StrictInt, StrictFloat
from typing import Union


class Error(BaseModel):
    code: int
    message: str
    status: str


class ErrorOut(BaseModel):
    error: Error
    

class AttributeInterface(BaseModel):
    remote_reference: str
    key: str
    value: Union[StrictInt, StrictFloat, StrictBool, str]


class AttributeIn(AttributeInterface):
    pass


class AttributeOut(AttributeInterface):
    id: int
    type: str

    class Config:
        orm_mode = True