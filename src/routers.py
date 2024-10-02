from utils import Routes
from src.common.router import router as common_router

__routes__ = Routes(routers=(common_router,))

__ws_routes__ = Routes(routers=())
