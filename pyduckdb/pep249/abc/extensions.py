"""
Sanctioned extensions to the DB-API 2.0, as outlined in PEP-249.

https://www.python.org/dev/peps/pep-0249/#optional-db-api-extensions

"""
# pylint: disable=bad-continuation
from abc import abstractmethod, ABCMeta
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .connection import Connection


class ConnectionErrorsMixin(metaclass=ABCMeta):
    # pylint: disable=too-few-public-methods,invalid-name,missing-function-docstring
    """
    An optional extension to PEP-249, providing access to mandated
    exception types as members of the Connection class.

    """

    @property
    @abstractmethod
    def Error(self) -> Type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def InterfaceError(self) -> Type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def DatabaseError(self) -> Type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def DataError(self) -> Type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def OperationalError(self) -> Type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def IntegrityError(self) -> Type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def InternalError(self) -> Type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def ProgrammingError(self) -> Type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def NotSupportedError(self) -> Type[Exception]:
        raise NotImplementedError


# pylint: disable=too-few-public-methods
class CursorConnectionMixin(metaclass=ABCMeta):
    """
    An optional extension of PEP-249 which attaches a read only
    reference to the Connection object the cursor was created from.

    """

    @property
    def connection(self) -> "Connection":
        """The parent Connection of the implementing cursor."""
        raise NotImplementedError
