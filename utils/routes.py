from fastapi import FastAPI
from dataclasses import dataclass
from src.config.settings import SETTINGS
from typing import Tuple


@dataclass(frozen=True)
class Routes:
    routers: Tuple

    def register_routes(self, app: FastAPI, prefix=SETTINGS.API_V1_STR):
        for router in self.routers:
            app.include_router(router, prefix=prefix)
