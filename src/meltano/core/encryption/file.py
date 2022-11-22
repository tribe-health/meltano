from __future__ import annotations

from meltano.core.encryption.base import EncryptionKey


class FileEncryptionKey(EncryptionKey):
    def __init__(self, file: str):
        self.file = file

    @classmethod
    def from_uri(cls, key_uri: str) -> FileEncryptionKey:
        ...

    def encrypt(self, data):
        ...

    def decrypt(self, data):
        ...
