import inspect

import asyncpg

from develop import environment


async def create_pool_async() -> asyncpg.pool.Pool:
    method: str = inspect.currentframe().f_code.co_name
    result = await asyncpg.create_pool(
        min_size=1,
        max_size=10,
        host=environment.try_get_value(environment.KEY_POSTGRES_HOST),
        port=environment.try_get_value(environment.KEY_POSTGRES_PORT),
        database=environment.try_get_value(environment.KEY_POSTGRES_DATABASE),
        user=environment.try_get_value(environment.KEY_POSTGRES_USER),
        password=environment.try_get_value(environment.KEY_POSTGRES_PASSWORD)
    )
    print(method)
    return result


