"""
This module covers the exceptions outlined in PEP-249.

It also includes a function to convert DuckDB's pybind11-generated
RuntimeErrors to true exception types, and a decorator to do this
implicitly by wrapping functions.

"""
# pylint: disable=missing-class-docstring
from functools import wraps
from typing import Callable, TypeVar
from pyduckdb.pep249 import exceptions


INTEGRITY_ERRORS = ("Constraint Error",)
PROGRAMMING_ERRORS = (
    "Parser Error",
    "Binder Error",
    "Catalog Error",
    "TransactionContext Error",
)
DATA_ERRORS = ("Invalid Input Error", "Out of Range Error")
INTERNAL_ERRORS = ()
OPERATIONAL_ERRORS = ()
NOT_SUPPORTED_ERRORS = ()


__all__ = [
    "DatabaseError",
    "DataError",
    "Error",
    "InterfaceError",
    "IntegrityError",
    "InternalError",
    "NotSupportedError",
    "OperationalError",
    "ProgrammingError",
    "CONNECTION_CLOSED",
    "parse_runtime_error",
    "convert_runtime_errors",
]


class Error(exceptions.Error):
    pass


class InterfaceError(exceptions.InterfaceError):
    pass


class DatabaseError(exceptions.DatabaseError, RuntimeError):
    pass


class DataError(exceptions.DataError):
    pass


class OperationalError(exceptions.OperationalError):
    pass


class IntegrityError(exceptions.IntegrityError):
    pass


class InternalError(exceptions.InternalError):
    pass


class ProgrammingError(exceptions.ProgrammingError):
    pass


# pylint: disable=too-many-ancestors
class NotSupportedError(exceptions.NotSupportedError, NotImplementedError):
    pass


CONNECTION_CLOSED = ProgrammingError("Cannot operate on a closed connection.")


def parse_runtime_error(error: RuntimeError) -> DatabaseError:
    """
    Parse a runtime error straight from DuckDB and return a more
    appropriate exception.

    """
    if not isinstance(error, RuntimeError):
        return error
    error_string = str(error)
    error_type, *error_components = error_string.split(":")
    error_message = ":".join(error_components).lstrip()

    if error_type == "connection closed":
        return CONNECTION_CLOSED

    new_error_type = DatabaseError
    if error_type in INTEGRITY_ERRORS:
        new_error_type = IntegrityError
    elif error_type in PROGRAMMING_ERRORS:
        new_error_type = ProgrammingError
    elif error_type in DATA_ERRORS:
        new_error_type = DataError
    elif error_type in INTERNAL_ERRORS:
        new_error_type = InternalError
    elif error_type in OPERATIONAL_ERRORS:
        new_error_type = OperationalError
    elif error_type in NOT_SUPPORTED_ERRORS:
        new_error_type = NotSupportedError

    if "read-only mode" in error_type:
        new_error_type = ProgrammingError
        error_message = error_type

    return new_error_type(error_message)


ReturnType = TypeVar("ReturnType")


def convert_runtime_errors(
    function: Callable[..., ReturnType]
) -> Callable[..., ReturnType]:
    """Wrap a function, raising correct errors from `RuntimeError`s."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except RuntimeError as err:
            raise parse_runtime_error(err) from err

    return wrapper
