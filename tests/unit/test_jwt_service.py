import pytest
import jwt
from datetime import datetime, timedelta, timezone

from app.features.auth.domain.exceptions.auth_exception import InvalidTokenException
from app.features.auth.infrastructure.security.jwt_token_service import (
    JwtTokenService,
)


def test_jwt_access_and_refresh_token():
    service = JwtTokenService(
        secret_key="secret123456789012345678901234567890",
        algorithm="HS256",
        access_token_expire_minutes=10,
        refresh_token_expire_days=1,
    )

    access_token = service.create_access_token(
        subject="1", role="admin", extra_claims={"email": "admin@example.com"}
    )
    refresh_token = service.create_refresh_token(
        subject="1", role="admin", extra_claims={"email": "admin@example.com"}
    )

    access_payload = service.decode_token(access_token, expected_type="access")
    assert access_payload["sub"] == "1"
    assert access_payload["role"] == "admin"
    assert access_payload["type"] == "access"
    assert access_payload["email"] == "admin@example.com"

    refresh_payload = service.decode_token(refresh_token, expected_type="refresh")
    assert refresh_payload["sub"] == "1"
    assert refresh_payload["role"] == "admin"
    assert refresh_payload["type"] == "refresh"


def test_jwt_type_mismatch():
    service = JwtTokenService(
        secret_key="secret123456789012345678901234567890"
    )
    access_token = service.create_access_token(subject="1", role="user")

    with pytest.raises(InvalidTokenException) as exc_info:
        service.decode_token(access_token, expected_type="refresh")
    assert "Invalid token type" in str(exc_info.value)


def test_jwt_expired_token():
    service = JwtTokenService(
        secret_key="secret123456789012345678901234567890",
        access_token_expire_minutes=-10,
    )
    token = service.create_access_token(subject="1", role="user")

    with pytest.raises(InvalidTokenException) as exc_info:
        service.decode_token(token)
    assert "expired" in str(exc_info.value).lower()


def test_jwt_invalid_token():
    service = JwtTokenService(
        secret_key="secret123456789012345678901234567890"
    )
    with pytest.raises(InvalidTokenException):
        service.decode_token("not-a-valid-jwt-token")
