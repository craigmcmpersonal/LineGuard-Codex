# LineGuard Server

This directory contains a starter Flask application that will power the LineGuard React client.

## Getting started

1. Create a virtual environment: `python -m venv .venv`
2. Activate it and install dependencies: `pip install -r requirements.txt`
3. Run the development server: `python -m develop.run`

The app exposes a `/health` endpoint you can hit to verify the backend is alive.

## Project layout

- `develop/`: all production application code (Flask app, repositories, etc.).
- `test/`: placeholder for automated tests that exercise the code under `develop/`.

## Database access

`psycopg` is available for talking to PostgreSQL. Set a `DATABASE_URL` (e.g. `postgresql://postgres:password@localhost:5432/lineguard`) before creating repositories such as `MarketTypeRepository`, located in `develop/repositories/market_type_repository.py`.


