"""
Transaction support (and non-support!) for PEP-249 compliant database
API implementations.

These abstract mixin classes provide a context manager with

"""
from abc import ABCMeta, abstractmethod
from types import TracebackType
from typing import Optional, Type, TypeVar

TransactionMixinType = TypeVar(
    "TransactionMixinType", bound="TransactionFreeContextMixin"
)


# pylint: disable=too-few-public-methods
class TransactionFreeContextMixin(metaclass=ABCMeta):
    """
    A PEP-249 compliant 'transaction' protocol which does not implement
    transactions. In the standard, this protocol would be implemented by a
    database Cursor.

    Classes which implement this protocol will need to implement a `close`
    method, and will gain a context manager implementation.

    For a transaction-free context for use with connections, see
    `DummyTransactionContextMixin`.

    """

    @abstractmethod
    def close(self) -> None:
        """
        Close the connection.

        If there are un-commited changes, this should perform a rollback.

        """
        raise NotImplementedError

    def __enter__(self: TransactionMixinType) -> TransactionMixinType:
        """
        Allow the transaction-supporting object to be used as a context
        manager.
        """
        return self

    def __exit__(
        self,
        error_type: Optional[Type[BaseException]] = None,
        error: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> bool:
        """Close the object upon exiting the context manager."""
        self.close()
        return not error

    def __del__(self):
        """Close the object if it is garbage collected."""
        self.close()


class TransactionContextMixin(TransactionFreeContextMixin, metaclass=ABCMeta):
    """
    A PEP-249 compliant transaction protocol which implements implicitly-
    started transactions. In the standard, this protocol would be
    implemented by a database connection.

    Classes which implement this protocol will need to implement a `close`
    method, a `rollback` method, and a `commit method`; they will gain a
    context manager implementation which rolls back in event of an error.



    """

    @abstractmethod
    def commit(self) -> None:
        """
        Commit changes made since the start of the pending transaction.

        """
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """
        Roll back to the start of the pending transaction, discarding
        changes.

        """
        raise NotImplementedError

    def __exit__(
        self,
        error_type: Optional[Type[BaseException]] = None,
        error: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> bool:
        """
        Close the object upon exiting the context manager.

        If no exceptions were raised: try to commit the changes, rolling
        back if there is an issue with the commit, and close the connection.

        If an exception was raised: roll back, close the connection, re-raise
        the exception (by returning True).
        """
        if not error:
            try:
                self.commit()
            except:
                self.rollback()
                raise
            finally:
                self.close()
            return True

        try:
            self.rollback()
        finally:
            self.close()
        return False


class DummyTransactionContextMixin(TransactionContextMixin, metaclass=ABCMeta):
    """
    A PEP-249 compliant 'transaction' protocol which does not implement
    transactions, but pretends to. `commit` and `rollback` are both no-op
    functions. In the standard, this protocol would be implemented by a
    database connection without transaction support.

    Classes which implement this protocol will need to implement a `close`
    method, and will gain a context manager implementation.

    """

    def commit(self) -> None:
        return

    def rollback(self) -> None:
        return
