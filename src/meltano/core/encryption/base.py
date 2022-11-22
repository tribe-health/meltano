from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TypeVar
from urllib.parse import ParseResult, urlparse

__all__ = ["EncryptionKey"]

_T = TypeVar("_T", bound="EncryptionKey")


class EncryptionKey(metaclass=ABCMeta):
    """ABC for encryption keys."""

    scheme: str
    implementations: dict[str, _T] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "scheme"):
            raise TypeError(f"EncryptionKey subclass {cls} must define a scheme")

        cls.implementations[cls.scheme] = cls

    @staticmethod
    def is_encrypted(data: str) -> bool:
        return data.startswith("ENC(") and data.endswith(")")

    @staticmethod
    def prepare_encrypted(data: str) -> str:
        return data[4:-1]

    @classmethod
    @abstractmethod
    def from_uri(cls: type[_T], key_uri: ParseResult) -> _T:
        """Create an encryption key from a URI.

        key_uri: str
            The key URI to parse.

        Returns:
            The encryption key.
        """
        ...

    @abstractmethod
    def encrypt(self, data: str) -> str:
        ...

    @abstractmethod
    def decrypt(self, data: str) -> str:
        ...
