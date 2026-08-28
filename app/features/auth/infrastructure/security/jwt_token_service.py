from datetime import datetime, timedelta, timezone
from typing import Any, Optional, override
import jwt

from app.features.auth.domain.exceptions.auth_exception import InvalidTokenException
from app.features.auth.domain.interface.itoken_service import ITokenService


class JwtTokenService(ITokenService):
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    @override
    def create_access_token(
        self, subject: str, role: str, extra_claims: Optional[dict[str, Any]] = None
    ) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "sub": str(subject),
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
            "type": "access",
        }
        if extra_claims:
            payload.update(extra_claims)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    @override
    def create_refresh_token(
        self, subject: str, role: str, extra_claims: Optional[dict[str, Any]] = None
    ) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "sub": str(subject),
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
            "type": "refresh",
        }
        if extra_claims:
            payload.update(extra_claims)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    @override
    def decode_token(
        self, token: str, expected_type: Optional[str] = None
    ) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": True},
            )
            if expected_type and payload.get("type") != expected_type:
                raise InvalidTokenException(
                    f"Invalid token type: expected '{expected_type}', got '{payload.get('type')}'"
                )
            return payload
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("Token has expired")
        except jwt.InvalidTokenError as e:
            raise InvalidTokenException(f"Invalid token: {str(e)}")
