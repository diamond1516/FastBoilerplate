from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Any, Dict

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import CoreSchema, core_schema

from src.config import SETTINGS


class BaseFormat(ABC):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    @abstractmethod
    def __get_pydantic_json_schema__(
            cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def validate(cls, v=None, *args, **kwargs):
        raise NotImplementedError


class FileFieldFormatBase(BaseFormat):
    MEDIA_URL = SETTINGS.MEDIA_URL

    @classmethod
    def __get_pydantic_json_schema__(
            cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        return {"type": "url", "format": "url", "description": "URL to the file."}

    @classmethod
    def validate(cls, v=None, *args, **kwargs):
        return f'{SETTINGS.SERVER_HOST}/{cls.MEDIA_URL}{str(v)}'


class DateTimeFormat(BaseFormat):
    format = None

    @classmethod
    def __get_pydantic_json_schema__(
            cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        return {"type": "datetime", "format": "datetime", "description": "Datetime to the field."}

    @classmethod
    def validate(cls, v=None, *args, **kwargs):
        if not isinstance(v, (datetime, date)):
            raise TypeError('The value should be a datetime.datetime or datetime.date')
        return v.strftime(cls.format) if cls.format else v

    @classmethod
    def set_format(cls, _format):
        """
        The function set The format of the date and time
        :param _format:
        :return: cls
        """

        cls.format = _format
        return cls

