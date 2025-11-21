import unittest

from asyncpg.pool import Pool

from develop.persistence.model.book import Book
from develop.persistence.book_storage_adapter import BookStorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier


class TestBookStorageAdapter(unittest.IsolatedAsyncioTestCase):
    async def test_book_storage_adapter_creates_book_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: BookStorageAdapter = BookStorageAdapter(connection)
            book: Book = await storage_adapter.create(name)
            self.assertIsNotNone(book)
            self.assertIsNotNone(book.key)
            try:
                self.assertEqual(name, book.name)
                initial_book: str = book.model_dump_json()
                print(initial_book)
            finally:
                await storage_adapter.try_delete(book)

    async def test_book_storage_adapter_finds_book_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: BookStorageAdapter = BookStorageAdapter(connection)
            book: Book = await storage_adapter.create(name)
            try:
                retrieved_book: Book = await storage_adapter.try_find(book.name)
                self.assertIsNotNone(retrieved_book)
                self.assertEqual(book.key, retrieved_book.key)
                self.assertEqual(book.name, retrieved_book.name)
            finally:
                await storage_adapter.try_delete(book)

    async def test_book_storage_adapter_gets_book_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: BookStorageAdapter = BookStorageAdapter(connection)
            book: Book = await storage_adapter.create(name)
            try:
                retrieved_book: Book = await storage_adapter.try_get(book.key)
                self.assertIsNotNone(retrieved_book)
                self.assertEqual(book.key, retrieved_book.key)
                self.assertEqual(book.name, retrieved_book.name)
            finally:
                await storage_adapter.try_delete(book)

    async def test_book_storage_adapter_updates_book_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: BookStorageAdapter = BookStorageAdapter(connection)
            book: Book = await storage_adapter.create(name)
            try:
                new_name: str = compose_unique_identifier()
                book.name = new_name
                revised_book: Book = await storage_adapter.update(book)
                self.assertIsNotNone(revised_book)
                self.assertEqual(book.key, revised_book.key)
                self.assertEqual(new_name, revised_book.name)
                retrieved_book: Book = await storage_adapter.try_get(book.key)
                self.assertIsNotNone(retrieved_book)
                self.assertEqual(new_name, retrieved_book.name)
            finally:
                await storage_adapter.try_delete(book)


if __name__ == '__main__':
    unittest.main()
