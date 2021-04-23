# pyduckdb

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python wrapper for DuckDB to add type hinting and more closely mirror SQLite.

Currently provides a (mostly) [PEP 249](https://www.python.org/dev/peps/pep-0249/) compliant implementation of a
`Connection` and `Cursor`.

Differences from the PEP:
 - `Connection`s implement the `execute*()` functions from the cursor, and return a cursor, as SQLite does.
 - `Connection`s and `Cursor`s implement `executescript()` as SQLite does.
 - `Cursor`s implement the same transactional features as their `Connection`s.