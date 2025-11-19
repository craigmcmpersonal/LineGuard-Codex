import unittest

from asyncpg import Pool

from develop.repository.postgresql_pool_factory import PostgreSqlPoolFactory


class TestPostgreSqlConnection(unittest.IsolatedAsyncioTestCase):
    async def test_connection_works(self):
        pool_factory: PostgreSqlPoolFactory = await PostgreSqlPoolFactory.get_instance()
        pool: Pool = await pool_factory.get_pool()
        async with pool.acquire() as connection:
            self.assertIsNotNone(connection)


if __name__ == '__main__':
    unittest.main()
