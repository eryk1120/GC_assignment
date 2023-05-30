import base64
import random
import secrets

from typing import Protocol

from cryptography.fernet import Fernet


class RandomIntGenerator(Protocol):
    def generate_random_int(self, ending: int, beginning: int = 0) -> int:
        ...


class PseudoRandomIntGenerator:
    def generate_random_int(self, ending: int, beginning: int = 0) -> int:
        return random.randint(beginning, ending)


class SecretRandomIntGenerator:
    def generate_random_int(self, ending: int, beginning: int = 0) -> int:
        return secrets.randbelow(ending - beginning + 1) + beginning


class SecureRandomIntGenerator:
    def __init__(self) -> None:
        self.key = Fernet(base64.urlsafe_b64encode(b"0123456789abcdef"))

    def generate_random_int(self, min_value: int, max_value: int) -> int:
        random_bytes = self.key.decrypt(self.key.encrypt(b"0"))
        return (
            int.from_bytes(random_bytes, "big") % (max_value - min_value + 1)
            + min_value
        )
