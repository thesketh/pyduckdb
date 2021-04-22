"""
Connection and Cursor objects which fit the DB API spec.

"""
# pylint: disable=c-extension-no-member
from typing import Union
import duckdb
from duckdb import DuckDBPyConnection  # pylint: disable=no-name-in-module


__all__ = [
    "Connection",
    "Cursor"
]


class Connection:
    """
    A DB API 2.0 compliant connection for DuckDB, as outlined in PEP-249.

    """
    def __init__(self, database: Union[DuckDBPyConnection, str]):
        if isinstance(database, DuckDBPyConnection):
            self._connection = database
        else:
            self._connection = duckdb.connect(database)
        self._is_closed = False

    def close(self):
        """Close the database connection."""
        if self._is_closed:
            return
        self._connection.close()
        self._is_closed = True
