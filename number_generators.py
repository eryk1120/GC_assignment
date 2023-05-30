import secrets

from typing import Protocol


class RandomIntGenerator(Protocol):
    def generate_random_int(self, ending: int, beginning: int = 0) -> int:
        ...


class SecretRandomIntGenerator:
    def generate_random_int(self, ending: int, beginning: int = 0) -> int:
        return secrets.randbelow(ending - beginning + 1) + beginning
