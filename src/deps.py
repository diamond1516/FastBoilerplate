from typing import AsyncGenerator, Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.db import db_helper
from fastapi import Depends


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = db_helper.get_scoped_session()
    try:
        yield session
    finally:
        await session.close()


Database = Annotated[Union[AsyncSession, None], Depends(get_db)]

