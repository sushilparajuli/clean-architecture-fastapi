from typing import Optional, override
import pytest

from app.features.auth.application.auth_service import AuthService
from app.features.auth.domain.exceptions.auth_exception import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserInactiveException,
)
from app.features.auth.domain.interface.iuser_repository import IUserRepository
from app.features.auth.domain.user_entity import UserEntity
from app.features.auth.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from app.features.auth.infrastructure.security.jwt_token_service import (
    JwtTokenService,
)


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users: dict[int, UserEntity] = {}
        self.counter = 1

    @override
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        return self.users.get(user_id)

    @override
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    @override
    def create_user(self, user: UserEntity) -> UserEntity:
        user_id = self.counter
        self.counter += 1
        created = UserEntity(
            id=user_id,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role,
            is_active=user.is_active,
        )
        self.users[user_id] = created
        return created

    @override
    def update_user(self, user_id: int, user: UserEntity) -> UserEntity:
        if user_id in self.users:
            self.users[user_id] = user
            return user
        raise ValueError("User not found")


@pytest.fixture
def auth_service() -> AuthService:
    user_repo = InMemoryUserRepository()
    hasher = BcryptPasswordHasher(rounds=4)
    token_service = JwtTokenService(
        secret_key="unit-test-secret-key-very-secure-1234567890",
        access_token_expire_minutes=15,
        refresh_token_expire_days=7,
    )
    return AuthService(
        user_repository=user_repo,
        password_hasher=hasher,
        token_service=token_service,
    )


def test_register_and_login_success(auth_service: AuthService):
    user = auth_service.register(
        email="john@example.com", password="password123", role="user"
    )
    assert user.id is not None
    assert user.email == "john@example.com"
    assert user.role == "user"

    access_token, refresh_token, logged_in_user = auth_service.login(
        email="john@example.com", password="password123"
    )
    assert access_token is not None
    assert refresh_token is not None
    assert logged_in_user.id == user.id


def test_register_duplicate_email(auth_service: AuthService):
    auth_service.register(
        email="duplicate@example.com", password="password123"
    )
    with pytest.raises(UserAlreadyExistsException):
        auth_service.register(
            email="duplicate@example.com", password="password456"
        )


def test_login_wrong_password(auth_service: AuthService):
    auth_service.register(email="wrongpass@example.com", password="password123")
    with pytest.raises(InvalidCredentialsException):
        auth_service.login(email="wrongpass@example.com", password="wrongpassword")


def test_login_inactive_user(auth_service: AuthService):
    user = auth_service.register(
        email="inactive@example.com", password="password123"
    )
    user.is_active = False
    auth_service.user_repository.update_user(user.id, user)

    with pytest.raises(UserInactiveException):
        auth_service.login(email="inactive@example.com", password="password123")


def test_refresh_token_flow(auth_service: AuthService):
    auth_service.register(email="refresh@example.com", password="password123")
    _, refresh_token, _ = auth_service.login(
        email="refresh@example.com", password="password123"
    )

    new_access, new_refresh, user = auth_service.refresh(refresh_token)
    assert new_access is not None
    assert new_refresh is not None
    assert user.email == "refresh@example.com"


def test_get_current_user(auth_service: AuthService):
    auth_service.register(email="me@example.com", password="password123")
    access_token, _, _ = auth_service.login(
        email="me@example.com", password="password123"
    )

    current_user = auth_service.get_current_user(access_token)
    assert current_user.email == "me@example.com"
