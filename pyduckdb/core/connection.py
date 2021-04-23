"""
Connection object for DuckDB which fits the DB API spec.

"""
# pylint: disable=c-extension-no-member
from typing import Optional, Sequence, Union
import duckdb
from duckdb import DuckDBPyConnection  # pylint: disable=no-name-in-module
from pyduckdb.pep249.abc import (
    ConnectionErrorsMixin,
    Connection as AbstractConnection,
    CursorExecuteMixin,
)
from pyduckdb.pep249.abc.types import (
    SQLQuery,
    QueryParameters,
    ProcName,
    ProcArgs,
)
from pyduckdb.core.cursor import Cursor
from pyduckdb.core.exceptions import (
    Error,
    InterfaceError,
    DatabaseError,
    DataError,
    OperationalError,
    IntegrityError,
    InternalError,
    ProgrammingError,
    NotSupportedError,
    CONNECTION_CLOSED,
    parse_runtime_error,
)

__all__ = ["Connection"]


class Connection(ConnectionErrorsMixin, AbstractConnection, CursorExecuteMixin):
    """
    A DB API 2.0 compliant connection for DuckDB, as outlined in
    PEP 249.

    Can be constructed by passing a database string or a
    DuckDBPyConnection.

    Accepts a read_only kwarg, which defaults to False. This argument
    is only valid if passed a database string, and will raise an error
    otherwise.

    """

    Error = Error
    InterfaceError = InterfaceError
    DatabaseError = DatabaseError
    DataError = DataError
    OperationalError = OperationalError
    IntegrityError = IntegrityError
    InternalError = InternalError
    ProgrammingError = ProgrammingError
    NotSupportedError = NotSupportedError

    def __init__(
        self,
        database: Union[DuckDBPyConnection, str],
        *,
        read_only: Optional[bool] = None
    ):
        if isinstance(database, DuckDBPyConnection):
            if read_only is not None:
                raise InterfaceError(
                    "`read_only` flag can only be set for database strings."
                )
            self._connection = database
        else:
            self._connection = duckdb.connect(database, bool(read_only))
        self._closed = False

    def close(self) -> None:
        """Close the database connection."""
        if self._closed:
            return
        self.rollback()
        self._connection.close()
        self._closed = True

    def commit(self) -> None:
        if self._closed:
            raise CONNECTION_CLOSED
        self._connection.commit()

    def rollback(self) -> None:
        if self._closed:
            raise CONNECTION_CLOSED
        try:
            self._connection.rollback()
        except RuntimeError as err:
            # Ignore this - no open transaction to roll back.
            if str(err).startswith("TransactionContext Error:"):
                return
            raise parse_runtime_error(err) from err

    def cursor(self) -> Cursor:
        if self._closed:
            raise CONNECTION_CLOSED
        try:
            return Cursor(self, self._connection.cursor())
        except RuntimeError as err:
            raise parse_runtime_error(err) from err

    def callproc(
        self, procname: ProcName, parameters: Optional[ProcArgs] = None
    ) -> Optional[ProcArgs]:
        return self.cursor().execute(procname, parameters)

    def execute(
        self, operation: SQLQuery, parameters: Optional[QueryParameters] = None
    ) -> Cursor:
        return self.cursor().execute(operation, parameters)

    def executescript(self, script: SQLQuery):
        """A lazy implementation of SQLite's `executescript`."""
        return self.execute(script)

    def executemany(
        self, operation: SQLQuery, seq_of_parameters: Sequence[QueryParameters]
    ) -> Cursor:
        return self.cursor().executemany(operation, seq_of_parameters)
