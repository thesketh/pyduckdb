"""
This module covers the exceptions outlined in PEP-249.

"""


__all__ = [
    "Error",
    "InterfaceError",
    "DatabaseError",
    "DataError",
    "OperationalError",
    "IntegrityError",
    "InternalError",
    "ProgrammingError",
    "NotSupportedError",
]


class Error(BaseException):
    """Base error outlined in PEP-249."""


class InterfaceError(Error):
    """
    Interface error outlined in PEP-249.

    Raised for errors with the database interface.

    """


class DatabaseError(Error, RuntimeError):
    """
    Database error outlined in PEP-249.

    Raised for errors with the database. This error is also a subclass
    of RuntimeError for consistency with DuckDB's Python wrapper.

    """


class DataError(DatabaseError):
    """
    Data error outlined in PEP-249.

    Raised for errors that are due to problems with processed data.

    """


class OperationalError(DatabaseError):
    """
    Operational error outlined in PEP-249.

    Raised for errors in the database's operation.

    """


class IntegrityError(DatabaseError):
    """
    Integrity error outlined in PEP-249.

    Raised when errors occur which affect the relational integrity of
    the database.

    """


class InternalError(DatabaseError):
    """
    Integrity error outlined in PEP-249.

    Raised when the database encounters an internal error.

    """


class ProgrammingError(DatabaseError):
    """
    Programming error outlined in PEP-249.

    Raised for SQL programming errors.

    """


class NotSupportedError(DatabaseError):
    """
    Not supported error outlined in PEP-249.

    Raised when an unsupported operation is attempted.

    """
