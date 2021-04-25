"""
Pure Python wrapper around DuckDB's pybind11 generated wrapper.

This API is intended to eventually be a drop-in replacement for SQLite
in most cases.

"""
from pep249.type_constructors import *
from pyduckdb.core import *

__all__ = [
    "apilevel",
    "threadsafety",
    "paramstyle",
    "connect",
    "Connection",
    "Cursor",
    "TimestampFromTicks",
    "TimeFromTicks",
    "DateFromTicks",
    "Date",
    "Time",
    "Timestamp",
    "ROWID",
    "DATETIME",
    "NUMBER",
    "BINARY",
    "STRING",
    "Binary",
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

__version__ = "0.0.1b3"

# pylint: disable=invalid-name
apilevel = "2.0"
threadsafety = 1
paramstyle = "qmark"


def connect(connection_string: str = ":memory:", read_only=False) -> Connection:
    """Connect to a DuckDB database, returning a connection."""
    return Connection(connection_string, read_only=read_only)
