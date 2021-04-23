"""
An abstract database connection implementation, conformant with PEP-249.

"""
# pylint: disable=bad-continuation
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING
from .transactions import TransactionContextMixin

if TYPE_CHECKING:
    from pyduckdb.pep249.abc.cursor import Cursor


class Connection(TransactionContextMixin, metaclass=ABCMeta):
    """A PEP-249 compliant Connection protocol."""

    @abstractmethod
    def cursor(self) -> "Cursor":
        """Return a database cursor."""
        raise NotImplementedError
