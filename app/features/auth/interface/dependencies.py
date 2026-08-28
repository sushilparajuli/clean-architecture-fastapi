from typing import Annotated, Optional
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config.env_config import EnvConfig
from app.core.providers.db import get_db_session
from app.core.providers.env_config import get_env_config
from app.features.auth.application.auth_service import AuthService
from app.features.auth.domain.exceptions.auth_exception import (
    InsufficientPermissionsException,
    InvalidTokenException,
    UserInactiveException,
)
from app.features.auth.domain.interface.iaudit_log_repository import (
    IAuditLogRepository,
)
from app.features.auth.domain.interface.ipassword_hasher import IPasswordHasher
from app.features.auth.domain.interface.itoken_service import ITokenService
from app.features.auth.domain.interface.iuser_repository import IUserRepository
from app.features.auth.domain.user_entity import UserEntity
from app.features.auth.infrastructure.repositories.audit_log_repository import (
    AuditLogRepository,
)
from app.features.auth.infrastructure.repositories.user_repository import (
    UserRepository,
)
from app.features.auth.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from app.features.auth.infrastructure.security.jwt_token_service import (
    JwtTokenService,
)

http_bearer_scheme = HTTPBearer(auto_error=False)


def get_user_repository(
    db_session: Annotated[Session, Depends(get_db_session)],
) -> IUserRepository:
    return UserRepository(session=db_session)


def get_audit_log_repository(
    db_session: Annotated[Session, Depends(get_db_session)],
) -> IAuditLogRepository:
    return AuditLogRepository(session=db_session)


def get_password_hasher(
    config: Annotated[EnvConfig, Depends(get_env_config)],
) -> IPasswordHasher:
    return BcryptPasswordHasher(rounds=config.bcrypt_rounds)


def get_token_service(
    config: Annotated[EnvConfig, Depends(get_env_config)],
) -> ITokenService:
    return JwtTokenService(
        secret_key=config.jwt_secret_key,
        algorithm=config.jwt_algorithm,
        access_token_expire_minutes=config.access_token_expire_minutes,
        refresh_token_expire_days=config.refresh_token_expire_days,
    )


def get_auth_service(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
    password_hasher: Annotated[IPasswordHasher, Depends(get_password_hasher)],
    token_service: Annotated[ITokenService, Depends(get_token_service)],
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )


def get_current_user(
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(http_bearer_scheme)
    ],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserEntity:
    if not credentials or not credentials.credentials:
        raise InvalidTokenException("Missing or invalid Authorization header")

    user = auth_service.get_current_user(credentials.credentials)
    if not user.is_active:
        raise UserInactiveException()

    return user


def require_admin(
    current_user: Annotated[UserEntity, Depends(get_current_user)],
) -> UserEntity:
    if current_user.role != "admin":
        raise InsufficientPermissionsException("Admin privileges required")
    return current_user
