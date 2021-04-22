"""
An abstract database API implementation.

"""
from collections.abc import ABCMeta, abstractmethod

class AbstractConnection(metaclass=ABCMeta):
    """A PEP-249 compliant Connection protocol."""
    @abstractmethod
    def close(self) -> None:
        """
        Close the database connection.

        If there are un-commited changes, perform a rollback.

        """
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        """Commit changes since the last transaction."""
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """Roll back to the start of the pending transaction."""
        raise NotImplementedError

    @abstractmethod
    def cursor(self) -> 'AbstractCursor':
        """Return a database cursor."""
        raise NotImplementedError


class AbstractCursor(metaclass=ABCMeta):
    """A PEP-249 compliant Cursor protocol."""