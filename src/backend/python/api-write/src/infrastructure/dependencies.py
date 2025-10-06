from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.repositories.postgres_order_repository import PostgresOrderRepository, SqlOrderRepository
from infrastructure.database import AsyncSessionLocal, get_postgres_session

async def get_order_repository(session: AsyncSession = Depends(get_postgres_session)):
    return PostgresOrderRepository(session)

# async def get_order_repository():
#     return SqlOrderRepository(session_factory=AsyncSessionLocal)
