"""
Core functionality implemented by pyduckdb.

This is mostly the concrete implementation of the DB 2.0 API.

"""
from .connection import Connection
from .cursor import Cursor
from .exceptions import (
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

__all__ = [
    "Connection",
    "Cursor",
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
