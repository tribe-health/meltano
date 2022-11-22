from __future__ import annotations

from urllib.parse import ParseResult

from cryptography import fernet

from meltano.core.encryption.base import EncryptionKey


class FernetEncryptionKey(EncryptionKey):
    scheme = "fernet"

    def __init__(self, key: str):
        self.value = fernet.MultiFernet([fernet.Fernet(k) for k in key.split(",")])

    @classmethod
    def from_uri(
        cls: type[FernetEncryptionKey],
        key_uri: ParseResult,
    ) -> FernetEncryptionKey:
        return cls(key_uri.netloc)

    def encrypt(self, data: str) -> str:
        return self.value.encrypt(data.encode()).decode()

    def decrypt(self, data: str) -> str:
        return self.value.decrypt(data).decode()
