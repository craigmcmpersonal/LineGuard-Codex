"""Data access helpers for the Market_Type table."""

from __future__ import annotations

import os
from typing import Any, Optional

import psycopg
from psycopg.rows import dict_row


class MarketTypeRepository:
    """Repository providing CRUD helpers for the Market_Type table."""

    def __init__(self, dsn: Optional[str] = None) -> None:
        self._dsn = dsn or os.getenv("DATABASE_URL")
        if not self._dsn:
            raise ValueError(
                "A PostgreSQL connection string is required. "
                "Set the DATABASE_URL environment variable or pass a DSN explicitly."
            )

    def _get_connection(self) -> psycopg.Connection[dict[str, Any]]:
        # Each call provides a fresh connection; callers can optimize by passing a custom factory.
        return psycopg.connect(self._dsn, row_factory=dict_row)

    def create(self, name: str) -> dict[str, Any]:
        """Insert a new market type and return the created record."""
        query = 'INSERT INTO public."Market_Type" (name) VALUES (%s) RETURNING market_type_key, name;'
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name,))
                return cur.fetchone()

    def get_by_id(self, market_type_key: int) -> Optional[dict[str, Any]]:
        """Fetch a market type by its primary key."""
        query = 'SELECT market_type_key, name FROM public."Market_Type" WHERE market_type_key = %s;'
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (market_type_key,))
                return cur.fetchone()

    def get_by_name(self, name: str) -> Optional[dict[str, Any]]:
        """Fetch a market type by its unique name."""
        query = 'SELECT market_type_key, name FROM public."Market_Type" WHERE name = %s;'
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name,))
                return cur.fetchone()

    def list_all(self) -> list[dict[str, Any]]:
        """Return every market type ordered by name."""
        query = 'SELECT market_type_key, name FROM public."Market_Type" ORDER BY name;'
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def update(self, market_type_key: int, *, name: str) -> Optional[dict[str, Any]]:
        """Update a market type and return the updated record, if it exists."""
        query = (
            'UPDATE public."Market_Type" '
            "SET name = %s "
            "WHERE market_type_key = %s "
            "RETURNING market_type_key, name;"
        )
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, market_type_key))
                return cur.fetchone()

    def delete(self, market_type_key: int) -> bool:
        """Delete a market type by its primary key."""
        query = 'DELETE FROM public."Market_Type" WHERE market_type_key = %s;'
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (market_type_key,))
                return cur.rowcount > 0

