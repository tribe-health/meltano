from __future__ import annotations

from urllib.parse import urlparse

from meltano.core.encryption.base import EncryptionKey


def get_key(key_uri: str) -> EncryptionKey:
    parsed_uri = urlparse(key_uri)
    try:
        return EncryptionKey.implementations[parsed_uri.scheme].from_uri(parsed_uri)
    except KeyError:
        raise ValueError(f"Unknown encryption scheme: {parsed_uri.scheme}")
