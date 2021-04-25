"""
Pure Python wrapper around DuckDB's pybind11 generated wrapper. This
async implementation uses the sync implementation and asyncio.to_thread.

This API is intended to showcase the utility of the PEP 249 abstract
base classes.

"""
from pep249.type_constructors import *
from pyduckdb.core.exceptions import (
    DatabaseError,
    DataError,
    Error,
    InterfaceError,
    IntegrityError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
)
from .connection import AsyncConnection
from .cursor import AsyncCursor
from .. import __version__

__all__ = [
    "apilevel",
    "threadsafety",
    "paramstyle",
    "connect",
    "AsyncConnection",
    "AsyncCursor",
    "Binary",
    "STRING",
    "BINARY",
    "NUMBER",
    "DATETIME",
    "ROWID",
    "Date",
    "Time",
    "Timestamp",
    "DateFromTicks",
    "TimeFromTicks",
    "TimestampFromTicks",
    "Error",
    "InterfaceError",
    "DatabaseError",
    "DataError",
    "IntegrityError",
    "InternalError",
    "NotSupportedError",
    "OperationalError",
    "ProgrammingError",
]

# pylint: disable=invalid-name
apilevel = "2.0"
threadsafety = 1
paramstyle = "qmark"


def connect(connection_string: str = ":memory:", read_only=False) -> AsyncConnection:
    """Connect to a DuckDB database, returning an async connection."""
    return AsyncConnection(connection_string, read_only=read_only)
