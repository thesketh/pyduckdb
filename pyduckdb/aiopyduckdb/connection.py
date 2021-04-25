"""
Async connection object for DuckDB which fits the DB API spec.

"""
from typing import Optional, Union, Sequence
from duckdb import DuckDBPyConnection  # pylint: disable=no-name-in-module
from pep249 import aiopep249
from pep249.aiopep249 import (
    SQLQuery,
    ProcName,
    ProcArgs,
    QueryParameters,
)
from .cursor import AsyncCursor
from .utils import to_thread
from ..core.connection import Connection
from ..core.exceptions import InterfaceError


class AsyncConnection(aiopep249.AsyncCursorExecuteMixin, aiopep249.AsyncConnection):
    """
    A DB API 2.0 compliant async connection for DuckDB, as outlined in
    PEP 249.

    Can be constructed by passing a database string or, a pyduckdb.Connection,
    or a DuckDBPyConnection.

    Accepts a read_only kwarg, which defaults to False. This argument
    is only valid if passed a database string, and will raise an error
    otherwise.

    """

    def __init__(
        self,
        database: Union[DuckDBPyConnection, Connection, str],
        *,
        read_only: Optional[bool] = None
    ):
        if isinstance(database, (str, DuckDBPyConnection)):
            self._connection = Connection(database, read_only=read_only)
        else:
            if read_only is not None:
                raise InterfaceError(
                    "`read_only` flag can only be set for database strings."
                )
            self._connection = database

    async def commit(self) -> None:
        await to_thread(self._connection.commit)

    async def rollback(self) -> None:
        await to_thread(self._connection.rollback)

    async def close(self) -> None:
        await to_thread(self._connection.close)

    async def cursor(self) -> AsyncCursor:
        return AsyncCursor(self, self._connection.cursor())

    async def callproc(
        self, procname: ProcName, parameters: Optional[ProcArgs] = None
    ) -> Optional[ProcArgs]:
        cursor = await self.cursor()
        return await cursor.callproc(procname, parameters)

    async def execute(
        self, operation: SQLQuery, parameters: Optional[QueryParameters] = None
    ) -> AsyncCursor:
        cursor = await self.cursor()
        return await cursor.execute(operation, parameters)

    async def executescript(self, script: SQLQuery) -> AsyncCursor:
        """A lazy implementation of SQLite's `executescript`."""
        return await self.execute(script)

    async def executemany(
        self, operation: SQLQuery, seq_of_parameters: Sequence[QueryParameters]
    ) -> AsyncCursor:
        cursor = await self.cursor()
        return await cursor.executemany(operation, seq_of_parameters)
