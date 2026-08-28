from typing import override
import bcrypt

from app.features.auth.domain.interface.ipassword_hasher import IPasswordHasher


class BcryptPasswordHasher(IPasswordHasher):
    def __init__(self, rounds: int = 12):
        self.rounds = rounds

    @override
    def hash(self, plain_password: str) -> str:
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @override
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                hashed_password.encode("utf-8"),
            )
        except Exception:
            return False
