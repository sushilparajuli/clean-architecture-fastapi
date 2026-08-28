from typing import Annotated
from fastapi import Depends, status

from app.core.router.route import get_versioned_router
from app.features.auth.application.auth_service import AuthService
from app.features.auth.domain.user_entity import UserEntity
from app.features.auth.interface.dependencies import (
    get_auth_service,
    get_current_user,
)
from app.features.auth.interface.schemas import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

v1_router = get_versioned_router("v1")


@v1_router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def register(
    data: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserResponse:
    user = auth_service.register(
        email=data.email,
        password=data.password,
        role=data.role or "user",
    )
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@v1_router.post(
    "/auth/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    access_token, refresh_token, _ = auth_service.login(
        email=data.email,
        password=data.password,
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@v1_router.post(
    "/auth/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
def refresh(
    data: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    access_token, refresh_token, _ = auth_service.refresh(
        refresh_token=data.refresh_token
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@v1_router.get(
    "/auth/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def get_me(
    current_user: Annotated[UserEntity, Depends(get_current_user)],
) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )
