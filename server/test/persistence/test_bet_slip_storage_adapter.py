import unittest
import uuid
from decimal import Decimal

from asyncpg.pool import Pool

import develop.constants as constants
from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.model.bet_slip_source import BetSlipSource
from develop.persistence.model.bet_slip_status import BetSlipStatus
from develop.persistence.model.book import Book
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.persistence.storage_adapter import StorageAdapter
from develop.utility import compose_unique_identifier


class TestBetSlipStorageAdapter(unittest.IsolatedAsyncioTestCase):
    async def test_bet_slip_storage_adapter_creates_bet_slip_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await storage_adapter.book.create(name)
            self.assertIsNotNone(book)
            self.assertIsNotNone(book.key)
            try:
                user_key: uuid.UUID = uuid.uuid4()
                text: str = compose_unique_identifier()
                external_identifier: str = compose_unique_identifier()
                original: bytes = text.encode(constants.ENCODING_UTF8)
                bet_slip: BetSlip = await storage_adapter.bet_slip.create(
                    user_key,
                    book.key,
                    0,
                    0,
                    BetSlipStatus.PLACED,
                    original,
                    BetSlipSource.SYNC,
                    external_identifier=external_identifier
                )
                self.assertIsNotNone(bet_slip)
                self.assertIsNotNone(bet_slip.key)
                try:
                    serialized: str = bet_slip.model_dump_json()
                    print(serialized)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)

    async def test_book_storage_adapter_finds_bet_slip_record_by_book_identifier_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await storage_adapter.book.create(name)
            self.assertIsNotNone(book)
            self.assertIsNotNone(book.key)
            try:
                user_key: uuid.UUID = uuid.uuid4()
                text: str = compose_unique_identifier()
                external_identifier: str = compose_unique_identifier()
                original: bytes = text.encode(constants.ENCODING_UTF8)
                bet_slip: BetSlip = await storage_adapter.bet_slip.create(
                    user_key,
                    book.key,
                    0,
                    0,
                    BetSlipStatus.PLACED,
                    original,
                    BetSlipSource.SYNC,
                    external_identifier=external_identifier
                )
                self.assertIsNotNone(bet_slip)
                self.assertIsNotNone(bet_slip.key)
                try:
                    retrieved: list[BetSlip] = await storage_adapter.bet_slip.find_by_book_identifier(
                        user_key,
                        book.key,
                        external_identifier)
                    self.assertIsNotNone(retrieved)
                    if (count := len(retrieved)) != 1:
                        self.fail(count)
                    else:
                        self.assertEqual(bet_slip.key, retrieved[0].key)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)

    async def test_book_storage_adapter_finds_bet_slip_record_by_status_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await storage_adapter.book.create(name)
            self.assertIsNotNone(book)
            self.assertIsNotNone(book.key)
            try:
                user_key: uuid.UUID = uuid.uuid4()
                text: str = compose_unique_identifier()
                external_identifier: str = compose_unique_identifier()
                original: bytes = text.encode(constants.ENCODING_UTF8)
                bet_slip: BetSlip = await storage_adapter.bet_slip.create(
                    user_key,
                    book.key,
                    0,
                    0,
                    BetSlipStatus.PLACED,
                    original,
                    BetSlipSource.SYNC,
                    external_identifier=external_identifier
                )
                self.assertIsNotNone(bet_slip)
                self.assertIsNotNone(bet_slip.key)
                try:
                    retrieved: list[BetSlip] = await storage_adapter.bet_slip.find_by_status(user_key, bet_slip.status)
                    self.assertIsNotNone(retrieved)
                    if (count := len(retrieved)) != 1:
                        self.fail(count)
                    else:
                        self.assertEqual(bet_slip.key, retrieved[0].key)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)

    async def test_bet_slip_storage_adapter_gets_bet_slip_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await storage_adapter.book.create(name)
            self.assertIsNotNone(book)
            self.assertIsNotNone(book.key)
            try:
                user_key: uuid.UUID = uuid.uuid4()
                text: str = compose_unique_identifier()
                external_identifier: str = compose_unique_identifier()
                original: bytes = text.encode(constants.ENCODING_UTF8)
                bet_slip: BetSlip = await storage_adapter.bet_slip.create(
                    user_key,
                    book.key,
                    0,
                    0,
                    BetSlipStatus.PLACED,
                    original,
                    BetSlipSource.SYNC,
                    external_identifier=external_identifier
                )
                self.assertIsNotNone(bet_slip)
                self.assertIsNotNone(bet_slip.key)
                try:
                    retrieved: BetSlip = await storage_adapter.bet_slip.try_get(bet_slip.key)
                    self.assertIsNotNone(retrieved)
                    self.assertEqual(external_identifier, retrieved.external_identifier)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)

    async def test_bet_slip_storage_adapter_updates_bet_slip_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await storage_adapter.book.create(name)
            self.assertIsNotNone(book)
            self.assertIsNotNone(book.key)
            try:
                user_key: uuid.UUID = uuid.uuid4()
                text: str = compose_unique_identifier()
                external_identifier: str = compose_unique_identifier()
                original: bytes = text.encode(constants.ENCODING_UTF8)
                bet_slip: BetSlip = await storage_adapter.bet_slip.create(
                    user_key,
                    book.key,
                    0,
                    0,
                    BetSlipStatus.PLACED,
                    original,
                    BetSlipSource.SYNC,
                    external_identifier=external_identifier
                )
                self.assertIsNotNone(bet_slip)
                self.assertIsNotNone(bet_slip.key)
                try:
                    bet_slip.will_pay = Decimal(10.0)
                    retrieved: BetSlip = await storage_adapter.bet_slip.update(bet_slip)
                    self.assertIsNotNone(retrieved)
                    self.assertEqual(bet_slip.will_pay, retrieved.will_pay)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)


if __name__ == '__main__':
    unittest.main()
