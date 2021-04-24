# pyduckdb

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python wrapper for DuckDB to add type hinting and more closely mirror SQLite. This is still a rough work in
progress, but should highlight the utility of the [PEP 249](https://github.com/thesketh/pep249) abstract base
classes.

This implementation provides Python type hints, context managers, and more distinct cursor types on top of
DuckDB. This is not intended to be used in production, but as a test bed for some ideas and to demonstrate
the abstract base classes.

Differences from the PEP:
 - `Connection`s implement the `execute*()` functions from the cursor, and return a cursor, as SQLite does.
 - `Connection`s and `Cursor`s implement `executescript()` as SQLite does.
 - `Cursor`s implement the same transactional features as their `Connection`s.
