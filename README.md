# pyduckdb

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python wrapper for DuckDB to add type hinting and more closely mirror SQLite. This is still a rough work in
progress, but should hopefully highlight the utility of the [PEP 249](https://github.com/thesketh/pep249) 
abstract base classes.

This implementation provides Python type hints, context managers, and more distinct cursor types on top of
DuckDB. This is not intended to be used in production, but as a test bed for some ideas and to demonstrate
the abstract base classes.

## Installation

```
python3 -mpip install pyduckdb
```

## Usage

Uses the standard Python database API.

```python
from pyduckdb import connect

def main():
    with connect(":memory:") as connection:
        with connection.execute("SELECT 1;") as cursor:
            print(next(cursor))

if __name__ == "__main__":
    main()

```

There is a very naive async implementation available, which essentially involves wrapping every call
with [`asyncio.to_thread`](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread):

```python
import asyncio
from pyduckdb.aiopyduckdb import connect

async def main():
    async with connect(":memory:") as connection:
        async with await connection.execute("SELECT 1;") as cursor:
            print(await cursor.fetchone())

if __name__ == "__main__":
    asyncio.run(main())

```

Differences from the PEP:
 - `Connection`s implement the `execute*()` functions from the cursor, and return a cursor, as SQLite does.
 - `Connection`s and `Cursor`s implement `executescript()` as SQLite does.
 - `Cursor`s implement the same transactional features as their `Connection`s.
 