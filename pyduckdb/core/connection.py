"""
Connection object for DuckDB which fits the DB API spec.

"""
# pylint: disable=c-extension-no-member
from typing import Optional, Sequence, Union
import duckdb
from duckdb import DuckDBPyConnection  # pylint: disable=no-name-in-module
import pep249
from pep249 import (
    SQLQuery,
    QueryParameters,
    ProcName,
    ProcArgs,
)
from .cursor import Cursor
from .exceptions import InterfaceError, convert_runtime_errors
from .utils import raise_if_closed, ignore_transaction_error

__all__ = ["Connection"]


# pylint: disable=too-many-ancestors
class Connection(
    pep249.CursorExecuteMixin, pep249.ConcreteErrorMixin, pep249.Connection
):
    """
    A DB API 2.0 compliant connection for DuckDB, as outlined in
    PEP 249.

    Can be constructed by passing a database string or a
    DuckDBPyConnection.

    Accepts a read_only kwarg, which defaults to False. This argument
    is only valid if passed a database string, and will raise an error
    otherwise.

    """

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

    @raise_if_closed
    @convert_runtime_errors
    def commit(self) -> None:
        self._connection.commit()

    @raise_if_closed
    @ignore_transaction_error
    @convert_runtime_errors
    def rollback(self) -> None:
        self._connection.rollback()

    @convert_runtime_errors
    def close(self) -> None:
        """Close the database connection."""
        if self._closed:
            return

        try:
            # Rolling back unstaged commits.
            self.rollback()
            # Close the underlying DuckDB connection.
            self._connection.close()
        except ImportError:  # Underlying connection garbage collected.
            pass
        self._closed = True

    @raise_if_closed
    @convert_runtime_errors
    def cursor(self) -> Cursor:
        return Cursor(self, self._connection.cursor())

    def callproc(
        self, procname: ProcName, parameters: Optional[ProcArgs] = None
    ) -> Optional[ProcArgs]:
        return self.cursor().callproc(procname, parameters)

    def execute(
        self, operation: SQLQuery, parameters: Optional[QueryParameters] = None
    ) -> Cursor:
        return self.cursor().execute(operation, parameters)

    def executemany(
        self, operation: SQLQuery, seq_of_parameters: Sequence[QueryParameters]
    ) -> Cursor:
        return self.cursor().executemany(operation, seq_of_parameters)

    def executescript(self, script: SQLQuery) -> Cursor:
        """A lazy implementation of SQLite's `executescript`."""
        return self.execute(script)
