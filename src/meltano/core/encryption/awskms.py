from __future__ import annotations

from meltano.core.encryption.base import EncryptionKey


class AwsKmsEncryptionKey(EncryptionKey):
    def __init__(self, file: str):
        self.file = file

    @classmethod
    def from_uri(cls, key_uri: str) -> AwsKmsEncryptionKey:
        ...

    def encrypt(self, data):
        ...

    def decrypt(self, data):
        ...
