from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.staticfiles import StaticFiles
from src.routers import __routes__ as api_routes
from src.routers import __ws_routes__ as ws_routes
from datetime import datetime
from zoneinfo import ZoneInfo
from src.config.settings import SETTINGS


async def on_startup() -> None:
    print('The app is working 🏎🏎🏎🏎')


async def on_shutdown() -> None:
    print('The app is shutting down 🚌🚌🚌🚌')


class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_events(app)
        self.__register_routes(app)
        self.__register_ws_routes(app)
        self.__register_middlewares(app)
        self.__register_media_files(app)
        self.__register_static_files(app)
        add_pagination(self.__app)

    def get_app(self):
        return self.__app


    @staticmethod
    def __register_events(app: FastAPI):
        app.on_event('startup')(on_startup)
        app.on_event('shutdown')(on_shutdown)

    @staticmethod
    def __register_routes(app):
        api_routes.register_routes(app, prefix=SETTINGS.API_V1_STR)

    @staticmethod
    def __register_ws_routes(app):
        ws_routes.register_routes(app, prefix=SETTINGS.WS_PREFIX)

    @staticmethod
    def __register_middlewares(app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    def __register_media_files(app: FastAPI):
        app.mount(
            f'/{SETTINGS.MEDIA_URL}',
            StaticFiles(directory=f"{SETTINGS.MEDIA_URL}", check_dir=False),
            name="media",
        )

    @staticmethod
    def __register_static_files(app: FastAPI):
        app.mount(
            f'/{SETTINGS.STATIC_URL}',
            StaticFiles(directory=f"{SETTINGS.STATIC_URL}", check_dir=False),
            name="static",
        )

