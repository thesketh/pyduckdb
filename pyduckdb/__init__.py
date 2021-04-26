"""
Pure Python wrapper around DuckDB's pybind11 generated wrapper.

This API is intended to eventually be a drop-in replacement for SQLite
in most cases.

"""
import os
from typing import Union
from pep249.type_constructors import *
from .core import *

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


def connect(
    connection_string: Union[str, os.PathLike] = ":memory:", read_only: bool = False
) -> Connection:
    """Connect to a DuckDB database, returning a connection."""
    return Connection(connection_string, read_only=read_only)
