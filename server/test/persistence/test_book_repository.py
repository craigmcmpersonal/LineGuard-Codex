import unittest

from asyncpg.pool import Pool

from develop.persistance.model import Book
from develop.persistance.book_repository import BookRepository
from develop.persistance.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier


class TestBookRepository(unittest.IsolatedAsyncioTestCase):
    async def test_book_repository_creates_book_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: BookRepository = BookRepository(connection)
            book: Book = await repository.create(name)
            self.assertIsNotNone(book)
            self.assertIsNotNone(book.key)
            try:
                self.assertEqual(name, book.name)
                initial_book: str = book.model_dump_json()
                print(initial_book)
            finally:
                await repository.try_delete(book)

    async def test_book_repository_finds_book_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: BookRepository = BookRepository(connection)
            book: Book = await repository.create(name)
            try:
                retrieved_book: Book = await repository.try_find(book.name)
                self.assertIsNotNone(retrieved_book)
                self.assertEqual(book.key, retrieved_book.key)
                self.assertEqual(book.name, retrieved_book.name)
            finally:
                await repository.try_delete(book)

    async def test_book_repository_gets_book_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: BookRepository = BookRepository(connection)
            book: Book = await repository.create(name)
            try:
                retrieved_book: Book = await repository.try_get(book.key)
                self.assertIsNotNone(retrieved_book)
                self.assertEqual(book.key, retrieved_book.key)
                self.assertEqual(book.name, retrieved_book.name)
            finally:
                await repository.try_delete(book)

    async def test_book_repository_updates_book_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: BookRepository = BookRepository(connection)
            book: Book = await repository.create(name)
            try:
                new_name: str = compose_unique_identifier()
                book.name = new_name
                revised_book: Book = await repository.update(book)
                self.assertIsNotNone(revised_book)
                self.assertEqual(book.key, revised_book.key)
                self.assertEqual(new_name, revised_book.name)
                retrieved_book: Book = await repository.try_get(book.key)
                self.assertIsNotNone(retrieved_book)
                self.assertEqual(new_name, retrieved_book.name)
            finally:
                await repository.try_delete(book)


if __name__ == '__main__':
    unittest.main()
