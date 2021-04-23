"""
Pure Python wrapper around DuckDB's pybind11 generated wrapper.

This API is intended to eventually be a drop-in replacement for SQLite
in most cases.

"""
from pyduckdb.core import (
    Connection,
    Cursor,
    Error,
    InterfaceError,
    DatabaseError,
    DataError,
    IntegrityError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
)
from pyduckdb.type_constructors import (
    Date,
    Time,
    Timestamp,
    DateFromTicks,
    TimeFromTicks,
    TimestampFromTicks,
    Binary,
    STRING,
    BINARY,
    NUMBER,
    DATETIME,
    ROWID,
)

__all__ = [
    "apilevel",
    "threadsafety",
    "Connection",
    "Cursor",
    "connect",
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


def connect(connection_string: str = ":memory:", read_only=False) -> Connection:
    """Connect to a DuckDB database, returning a connection."""
    return Connection(connection_string, read_only=read_only)
