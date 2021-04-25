"""
Cursor object for DuckDB which fits the DB API spec.

"""
# pylint: disable=c-extension-no-member
import weakref
from typing import Optional, Sequence, Type, Union, TYPE_CHECKING
from duckdb import DuckDBPyConnection  # pylint: disable=no-name-in-module
import pep249
from pep249 import (
    SQLQuery,
    QueryParameters,
    ColumnDescription,
    ProcName,
    ProcArgs,
    ResultRow,
    ResultSet,
)
from .exceptions import (
    NotSupportedError,
    convert_runtime_errors,
)
from .utils import raise_if_closed, ignore_transaction_error

if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from pyduckdb.core.connection import Connection

__all__ = ["Cursor"]


# pylint: disable=too-many-ancestors
class Cursor(
    pep249.CursorConnectionMixin, pep249.IterableCursorMixin, pep249.TransactionalCursor
):
    """
    A DB API 2.0 compliant cursor for DuckDB, as outlined in
    PEP 249.

    Can be constructed by passing a Connection and a DuckDB 'cursor'
    (DuckDBPyConnection).

    """

    def __init__(self, connection: "Connection", duckdb_cursor: DuckDBPyConnection):
        self._connection = weakref.proxy(connection)
        self._cursor = duckdb_cursor
        self.__closed = False

    @property
    def _closed(self) -> bool:
        # pylint: disable=protected-access
        try:
            return self.__closed or self.connection._closed
        except ReferenceError:
            # Parent connection already GC'd.
            return True

    @_closed.setter
    def _closed(self, value: bool):
        self.__closed = value

    @property
    def connection(self) -> "Connection":
        return self._connection

    @property
    def description(self) -> Optional[Sequence[ColumnDescription]]:
        try:
            return self._cursor.description
        except RuntimeError:
            return None

    @property
    def rowcount(self) -> int:
        # DuckDB doesn't implement this functionality.
        return -1

    @raise_if_closed
    @convert_runtime_errors
    def commit(self) -> None:
        self._cursor.commit()

    @raise_if_closed
    @ignore_transaction_error
    @convert_runtime_errors
    def rollback(self) -> None:
        self._cursor.rollback()

    @convert_runtime_errors
    def close(self) -> None:
        """Close the cursor."""
        if self._closed:
            return

        try:
            # Rolling back unstaged commits.
            self.rollback()
            # Close the underlying DuckDB connection.
            self._cursor.close()
        except ImportError:  # Underlying connection garbage collected.
            pass
        self._closed = True

    def callproc(
        self, procname: ProcName, parameters: Optional[ProcArgs] = None
    ) -> Optional[ProcArgs]:
        raise NotSupportedError("DuckDB does not support stored procedures.")

    def nextset(self) -> Optional[bool]:
        raise NotSupportedError(
            "DuckDB Cursors do not support more than one result set."
        )

    @raise_if_closed
    def setinputsizes(self, sizes: Sequence[Optional[Union[int, Type]]]) -> None:
        pass

    @raise_if_closed
    def setoutputsize(self, size: int, column: Optional[int]) -> None:
        pass

    @raise_if_closed
    @convert_runtime_errors
    def execute(
        self, operation: SQLQuery, parameters: Optional[QueryParameters] = None
    ) -> "Cursor":
        if parameters is None:
            self._cursor.execute(operation)
        else:
            self._cursor.execute(operation, parameters)
        return self

    def executescript(self, script: SQLQuery) -> "Cursor":
        """A lazy implementation of SQLite's `executescript`."""
        return self.execute(script)

    @raise_if_closed
    @convert_runtime_errors
    def executemany(
        self, operation: SQLQuery, seq_of_parameters: Sequence[QueryParameters]
    ) -> "Cursor":
        self._cursor.executemany(operation, seq_of_parameters)
        return self

    @raise_if_closed
    @convert_runtime_errors
    def fetchone(self) -> Optional[ResultRow]:
        return self._cursor.fetchone()

    @raise_if_closed
    @convert_runtime_errors
    def fetchmany(self, size: Optional[int] = None) -> ResultSet:
        if size is None:
            size = self.arraysize
        return self._cursor.fetchmany(size)

    @raise_if_closed
    @convert_runtime_errors
    def fetchall(self) -> ResultSet:
        return self._cursor.fetchall()
