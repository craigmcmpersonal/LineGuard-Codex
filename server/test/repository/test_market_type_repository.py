import pytest
import pytest_asyncio
from asyncpg.pool import Pool

from develop.model.market_type import MarketType
from develop.repository import market_type_repository
from develop.repository.postgresql_pool_factory import PostgreSqlPoolFactory
from develop.utility import compose_unique_identifier


@pytest_asyncio.fixture
async def pool() -> Pool:
    """
    Shared asyncpg pool fixture.
    """
    factory = await PostgreSqlPoolFactory.get_instance()
    return await factory.get_pool()


@pytest.mark.asyncio
async def test_market_type_repository_creates_market_type_record(pool: Pool):
    name: str = compose_unique_identifier()

    async with pool.acquire() as connection:
        market_type: MarketType = await market_type_repository.create(name, connection)

        assert market_type is not None
        assert market_type.key is not None

        try:
            assert market_type.name == name
        finally:
            await market_type_repository.try_delete(market_type, connection)


@pytest.mark.asyncio
async def test_market_type_repository_finds_market_type_record(pool: Pool):
    name: str = compose_unique_identifier()

    async with pool.acquire() as connection:
        try:
            market_type: MarketType = await market_type_repository.create(name, connection)

            retrieved: MarketType = await market_type_repository.try_find(
                market_type.name,
                connection,
            )

            assert retrieved is not None
            assert retrieved.key == market_type.key
            assert retrieved.name == market_type.name

        finally:
            await market_type_repository.try_delete(market_type, connection)
