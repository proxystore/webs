from __future__ import annotations

from typing import Any
from typing import Protocol
from typing import runtime_checkable
from typing import TypeVar

K = TypeVar('K')
T = TypeVar('T')
IdentifierT = TypeVar('IdentifierT')


@runtime_checkable
class Transformer(Protocol[IdentifierT]):
    """Object transformer protocol."""

    def close(self) -> None:
        """Close the transformer.

        The transformer is only closed by the client once the application
        has finished executing (or raised an exception).
        """
        ...

    def is_identifier(self, obj: T) -> bool:
        """Check if the object is an identifier instance."""
        ...

    def transform(self, obj: T) -> IdentifierT:
        """Transform the object into an identifier.

        Args:
            obj: Object to transform.

        Returns:
            Identifier object that can be used to resolve `obj`.
        """
        ...

    def resolve(self, identifier: IdentifierT) -> Any:
        """Resolve an object from an identifier.

        Args:
            identifier: Identifier to an object.

        Returns:
            The resolved object.
        """
        ...
