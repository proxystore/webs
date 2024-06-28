from __future__ import annotations

from typing import Any
from typing import Literal
from typing import TypeVar

from proxystore.proxy import extract
from proxystore.proxy import Proxy
from proxystore.store import get_store
from proxystore.store import Store
from proxystore.store.config import ConnectorConfig
from pydantic import Field

from taps.plugins import register
from taps.transformer.config import TransformerConfig

T = TypeVar('T')


@register('transformer')
class ProxyTransformerConfig(TransformerConfig):
    """Proxy transformer configuration."""

    name: Literal['proxystore'] = Field(
        'proxystore',
        description='name of transformer type',
    )
    connector: ConnectorConfig = Field(
        description='connector configuration',
    )
    cache_size: int = Field(16, description='cache size')
    populate_target: bool = Field(
        True,
        description='populate target objects of newly created proxies',
    )
    extract_target: bool = Field(
        False,
        description=(
            'extract the target from the proxy when resolving the identifier'
        ),
    )

    def get_transformer(self) -> ProxyTransformer:
        """Create a transformer from the configuration."""
        connector = self.connector.get_connector()

        return ProxyTransformer(
            store=Store(
                'proxy-transformer',
                connector=connector,
                cache_size=self.cache_size,
                populate_target=self.populate_target,
                register=True,
            ),
            extract_target=self.extract_target,
        )


class ProxyTransformer:
    """Proxy object transformer.

    Transforms objects into proxies which act as the identifier.

    Args:
        store: Store instance to use for proxying objects.
        extract_target: When `True`, resolving an identifier (i.e., a proxy)
            will return the target object. Otherwise, the proxy is returned
            since a proxy can act as the target object.
    """

    def __init__(
        self,
        store: Store[Any],
        *,
        extract_target: bool = False,
    ) -> None:
        self.store = store
        self.extract_target = extract_target

    def __getstate__(self) -> dict[str, Any]:
        return {
            'config': self.store.config(),
            'extract_target': self.extract_target,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        store = get_store(state['config'].name)
        if store is not None:
            self.store = store
        else:
            self.store = Store.from_config(state['config'])
        self.extract_target = state['extract_target']

    def close(self) -> None:
        """Close the transformer."""
        self.store.close()

    def is_identifier(self, obj: Any) -> bool:
        """Check if the object is an identifier instance."""
        return isinstance(obj, Proxy)

    def transform(self, obj: T) -> Proxy[T]:
        """Transform the object into an identifier.

        Args:
            obj: Object to transform.

        Returns:
            Identifier object that can be used to resolve `obj`.
        """
        return self.store.proxy(obj)

    def resolve(self, identifier: Proxy[T]) -> T | Proxy[T]:
        """Resolve an object from an identifier.

        Args:
            identifier: Identifier to an object.

        Returns:
            The resolved object or a proxy of the resolved object depending \
            on the setting of `extract_target`.
        """
        return extract(identifier) if self.extract_target else identifier
