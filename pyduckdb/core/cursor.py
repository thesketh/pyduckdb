"""
Cursor object for DuckDB which fits the DB API spec.

"""
# pylint: disable=c-extension-no-member
import weakref
from typing import Optional, Sequence, Type, Union, TYPE_CHECKING
from duckdb import DuckDBPyConnection  # pylint: disable=no-name-in-module
from pyduckdb.pep249.abc import (
    Cursor as AbstractCursor,
    CursorConnectionMixin,
    TransactionContextMixin,
)
from pyduckdb.pep249.abc.types import (
    SQLQuery,
    QueryParameters,
    ColumnDescription,
    ProcName,
    ProcArgs,
    ResultRow,
    ResultSet,
)
from pyduckdb.core.exceptions import (
    NotSupportedError,
    CONNECTION_CLOSED,
    convert_runtime_errors,
    parse_runtime_error,
)

if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from pyduckdb.core.connection import Connection

__all__ = ["Cursor"]


# pylint: disable=too-many-ancestors
class Cursor(AbstractCursor, TransactionContextMixin, CursorConnectionMixin):
    """A database cursor."""

    def __init__(self, connection: "Connection", duckdb_cursor: DuckDBPyConnection):
        self._connection = weakref.ref(connection)
        self._cursor = duckdb_cursor
        self._closed = False

    @property
    def __closed(self) -> bool:
        # pylint: disable=protected-access
        parent = self.connection
        if parent is None:
            return True
        return self._closed or parent._closed

    @property
    def connection(self) -> Optional["Connection"]:
        return self._connection()

    @property
    def description(self) -> Optional[Sequence[ColumnDescription]]:
        if self.__closed:
            raise CONNECTION_CLOSED

        try:
            return self._cursor.description
        except RuntimeError:
            return None

    @property
    def rowcount(self) -> int:
        if self.__closed:
            raise CONNECTION_CLOSED
        return -1

    def commit(self) -> None:
        if self.__closed:
            raise CONNECTION_CLOSED
        self._cursor.commit()

    def rollback(self) -> None:
        if self.__closed:
            raise CONNECTION_CLOSED
        try:
            self._cursor.rollback()
        except RuntimeError as err:
            # Ignore this - no open transaction to roll back.
            if str(err).startswith("TransactionContext Error:"):
                return
            raise parse_runtime_error(err) from err

    def close(self) -> None:
        if self.__closed:
            return
        self._cursor.close()
        self._closed = True

    def callproc(
        self, procname: ProcName, parameters: Optional[ProcArgs] = None
    ) -> Optional[ProcArgs]:
        raise NotSupportedError("DuckDB does not support stored procedures.")

    def nextset(self) -> Optional[bool]:
        raise NotSupportedError(
            "DuckDB Cursors do not support more than one result set."
        )

    def setinputsizes(self, sizes: Sequence[Optional[Union[int, Type]]]) -> None:
        if self.__closed:
            raise CONNECTION_CLOSED

    def setoutputsize(self, size: int, column: Optional[int]) -> None:
        if self.__closed:
            raise CONNECTION_CLOSED

    @convert_runtime_errors
    def execute(
        self, operation: SQLQuery, parameters: Optional[QueryParameters] = None
    ) -> "Cursor":
        if self.__closed:
            raise CONNECTION_CLOSED

        if parameters is None:
            self._cursor.execute(operation)
        else:
            self._cursor.execute(operation, parameters)
        return self

    @convert_runtime_errors
    def executemany(
        self, operation: SQLQuery, seq_of_parameters: Sequence[QueryParameters]
    ) -> "Cursor":
        if self.__closed:
            raise CONNECTION_CLOSED

        self._cursor.executemany(operation, seq_of_parameters)
        return self

    @convert_runtime_errors
    def fetchone(self) -> Optional[ResultRow]:
        if self.__closed:
            raise CONNECTION_CLOSED

        return self._cursor.fetchone()

    @convert_runtime_errors
    def fetchmany(self, size: Optional[int] = None) -> ResultSet:
        if self.__closed:
            raise CONNECTION_CLOSED

        return self._cursor.fetchmany(size)

    @convert_runtime_errors
    def fetchall(self) -> ResultSet:
        if self.__closed:
            raise CONNECTION_CLOSED

        return self._cursor.fetchall()
