from pydantic import BaseModel
from fastapi import Query, HTTPException
from abc import ABC, abstractmethod
from itertools import chain
from typing import Any
import math


class AsyncBasePagination(ABC):
    response_schema: BaseModel = None

    @abstractmethod
    async def paginate(*args, **kwargs):
        raise NotImplementedError


class BasePagination(ABC):
    # response_schema: BaseModel = None

    @abstractmethod
    def paginate(self, *args, **kwargs):
        raise NotImplementedError


class PageNumberPagination(BasePagination, BaseModel):
    page_size: int = Query(10, gt=0)
    page: int = Query(1, gt=0)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.data = None
    #     self.len_data: int = 0

    @property
    def page_nums(self):
        return math.ceil(self.len_data / self.page_size)

    def paginate(self, data, *args, **kwargs):
        setattr(self, 'data', data)
        setattr(self, 'len_data', len(data))

        start_index = (self.page - 1) * self.page_size
        end_index = start_index + self.page_size

        try:
            items = data[start_index:end_index]
        except IndexError:
            raise HTTPException(status_code=404, detail="Invalid page")
        return list(items)
