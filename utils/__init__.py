__all__ = (
    'Routes',
    'now'
)

from datetime import datetime
from zoneinfo import ZoneInfo

from src.config.settings import SETTINGS
from .routes import Routes


def now(timezone: str = SETTINGS.TIME_ZONE):
    return datetime.now(ZoneInfo(timezone))
