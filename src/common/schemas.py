from datetime import datetime
from pydantic import BaseModel, Field
from fastapi_pagination import Params
from utils.customs import FileObject, DateTimeFormat
from fastapi import Query
from typing import (
    Optional, List
)


class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    image: FileObject

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    name: str
    email: str


class UserResSchema(UserCreateSchema):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class UserOrderSchema(BaseModel):
    id: int
    order_date: DateTimeFormat.set_format(_format='%Y-%m-%d %H:%M:%S')
    total_price: float

    class Config:
        from_attributes = True


class UserWithOrderSchema(BaseModel):
    id: int
    name: str
    email: str
    orders: List[UserOrderSchema]

    class Config:
        from_attributes = True
