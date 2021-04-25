"""
Async cursor object for DuckDB which fits the DB API spec.

"""
import weakref
from typing import Optional, Sequence, Type, Union, TYPE_CHECKING
from pep249 import aiopep249
from pep249.aiopep249 import (
    SQLQuery,
    ColumnDescription,
    ProcName,
    ProcArgs,
    QueryParameters,
    ResultRow,
    ResultSet,
)
from ..core.cursor import Cursor
from .utils import to_thread

if TYPE_CHECKING:
    from .connection import AsyncConnection  # pylint:disable=cyclic-import

# pylint: disable=too-many-ancestors
class AsyncCursor(
    aiopep249.CursorConnectionMixin,
    aiopep249.IterableAsyncCursorMixin,
    aiopep249.TransactionalAsyncCursor,
):
    """
    An async DB API 2.0 compliant cursor for DuckDB, as outlined in
    PEP 249.

    Can be constructed by passing an AsyncConnection and a sync Cursor.

    """

    def __init__(self, connection: "AsyncConnection", cursor: Cursor):
        self._connection = weakref.proxy(connection)
        self._cursor = cursor

    @property
    def connection(self) -> "AsyncConnection":
        return self._connection

    @property
    def description(self) -> Optional[Sequence[ColumnDescription]]:
        return self._cursor.description

    @property
    def rowcount(self) -> int:
        return self._cursor.rowcount

    async def commit(self) -> None:
        await to_thread(self._cursor.commit)

    async def rollback(self) -> None:
        await to_thread(self._cursor.rollback)

    async def close(self) -> None:
        await to_thread(self._cursor.close)

    async def callproc(
        self, procname: ProcName, parameters: Optional[ProcArgs] = None
    ) -> Optional[ProcArgs]:
        return await to_thread(self._cursor.callproc, procname, parameters)

    async def nextset(self) -> Optional[bool]:
        return await to_thread(self._cursor.nextset)

    def setinputsizes(self, sizes: Sequence[Optional[Union[int, Type]]]) -> None:
        self._cursor.setinputsizes(sizes)

    def setoutputsize(self, size: int, column: Optional[int] = None) -> None:
        self._cursor.setoutputsize(size, column)

    async def execute(
        self, operation: SQLQuery, parameters: Optional[QueryParameters] = None
    ) -> "AsyncCursor":
        await to_thread(self._cursor.execute, operation, parameters)
        return self

    async def executescript(self, script: SQLQuery) -> "AsyncCursor":
        """A lazy implementation of SQLite's `executescript`."""
        return await self.execute(script)

    async def executemany(
        self, operation: SQLQuery, seq_of_parameters: Sequence[QueryParameters]
    ) -> "AsyncCursor":
        await to_thread(self._cursor.executemany, operation, seq_of_parameters)
        return self

    async def fetchone(self) -> Optional[ResultRow]:
        return await to_thread(self._cursor.fetchone)

    async def fetchmany(self, size: Optional[int] = None) -> ResultSet:
        if size is None:
            size = self.arraysize
        return await to_thread(self._cursor.fetchmany, size)

    async def fetchall(self) -> ResultSet:
        return await to_thread(self._cursor.fetchall)
