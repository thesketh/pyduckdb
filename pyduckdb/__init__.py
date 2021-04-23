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

__all__ = [
    "Connection",
    "Cursor",
    "connect",
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


def connect(connection_string: str = ":memory:", read_only=False) -> Connection:
    """Connect to a DuckDB database, returning a connection."""
    return Connection(connection_string, read_only=read_only)
