from app.features.auth.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)


def test_bcrypt_hasher_hash_and_verify():
    hasher = BcryptPasswordHasher(rounds=4)
    plain = "SecurePassword123!"
    hashed = hasher.hash(plain)

    assert hashed != plain
    assert hasher.verify(plain, hashed) is True
    assert hasher.verify("WrongPassword123!", hashed) is False


def test_bcrypt_hasher_invalid_hash():
    hasher = BcryptPasswordHasher(rounds=4)
    assert hasher.verify("password", "invalid-hash-string") is False
