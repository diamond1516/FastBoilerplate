import os
from dataclasses import dataclass
from typing import Any, Dict

from PIL import Image
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import CoreSchema, core_schema
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator
from starlette.datastructures import UploadFile

from src.config import SETTINGS
from src.config.storages import LOCAL_STORAGE

SUPPORTED_IMAGE_EXTENSIONS = Image.registered_extensions()


@dataclass
class FileObject(object):
    MEDIA_URL = SETTINGS.MEDIA_URL if SETTINGS.MEDIA_URL.endswith('/') else SETTINGS.MEDIA_URL + '/'
    SERVER_HOST = SETTINGS.SERVER_HOST if SETTINGS.SERVER_HOST.endswith('/') else SETTINGS.SERVER_HOST + '/'
    path: str

    def __str__(self):
        return str(self.path)

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def url(self):
        return f'{self.SERVER_HOST}{self.MEDIA_URL}{self.path}'

    @property
    def extension(self):
        return os.path.splitext(self.path)[1]

    @property
    def size(self):
        file_path = os.path.join(self.MEDIA_URL, self.path)
        assert os.path.exists(file_path), f'File {file_path} does not exist'
        return os.path.getsize(file_path)

    @property
    def file(self):
        file_path = os.path.join(self.MEDIA_URL, self.path)
        return open(file_path, 'rb')

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(
            cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        return {"type": "url", "format": "url", "description": "URL to the file."}

    @classmethod
    def validate(cls, v=None, *args, **kwargs):
        return f'{cls.SERVER_HOST}{cls.MEDIA_URL}{str(v)}'


class FileField(TypeDecorator):
    impl = String

    def __init__(
            self,
            upload_to='',
            storage_manager=LOCAL_STORAGE,
            *args,
            **kwargs
    ):

        """
        :param upload_to:  folder name
        :param storage_manager: storage manager object
        :param args: extra arguments
        :param kwargs: extra keyword arguments
        """

        self.storage_manager = storage_manager
        self.upload_folder = upload_to

        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if isinstance(value, (UploadFile, FileObject)):
            file_path = self.storage_manager.save(value, self.upload_folder)
            return file_path
        return str(value)

    def process_result_value(self, value, dialect) -> FileObject:
        return FileObject(path=value)

