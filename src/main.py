from fastapi import FastAPI, Request
from src.config import SETTINGS
from src.config.server import Server


def app(_=None) -> FastAPI:
    main = FastAPI(
        title=SETTINGS.PROJECT_NAME,
        debug=SETTINGS.DEBUG,
        version=SETTINGS.VERSION
    )

    @main.get('/', include_in_schema=False)
    def index(request: Request):
        return {'docs': f'{request.url}docs'}
    return Server(main).get_app()
