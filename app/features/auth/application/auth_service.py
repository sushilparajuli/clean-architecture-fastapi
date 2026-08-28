from typing import Optional

from app.core.exceptions.repository import UniqueConstraintFailure
from app.features.auth.domain.exceptions.auth_exception import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserInactiveException,
    UserNotFoundException,
)
from app.features.auth.domain.interface.ipassword_hasher import IPasswordHasher
from app.features.auth.domain.interface.itoken_service import ITokenService
from app.features.auth.domain.interface.iuser_repository import IUserRepository
from app.features.auth.domain.user_entity import UserEntity


class AuthService:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def register(self, email: str, password: str, role: str = "user") -> UserEntity:
        """
        Register a new user
        :param email: user email
        :param password: user plaintext password
        :param role: user role ('user' or 'admin')
        :return: Created UserEntity
        """
        normalized_email = email.strip().lower()
        existing_user = self.user_repository.get_by_email(normalized_email)
        if existing_user:
            raise UserAlreadyExistsException(normalized_email)

        hashed_password = self.password_hasher.hash(password)
        new_user = UserEntity(
            email=normalized_email,
            hashed_password=hashed_password,
            role=role,
            is_active=True,
        )

        try:
            return self.user_repository.create_user(new_user)
        except UniqueConstraintFailure:
            raise UserAlreadyExistsException(normalized_email)

    def login(self, email: str, password: str) -> tuple[str, str, UserEntity]:
        """
        Authenticate user credentials and issue tokens
        :param email: user email
        :param password: user plaintext password
        :return: tuple of (access_token, refresh_token, user_entity)
        """
        normalized_email = email.strip().lower()
        user = self.user_repository.get_by_email(normalized_email)
        if not user or not user.hashed_password:
            raise InvalidCredentialsException()

        if not self.password_hasher.verify(password, user.hashed_password):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise UserInactiveException()

        access_token = self.token_service.create_access_token(
            subject=str(user.id),
            role=user.role,
            extra_claims={"email": user.email},
        )
        refresh_token = self.token_service.create_refresh_token(
            subject=str(user.id),
            role=user.role,
            extra_claims={"email": user.email},
        )

        return access_token, refresh_token, user

    def refresh(self, refresh_token: str) -> tuple[str, str, UserEntity]:
        """
        Validate refresh token and issue a new token pair
        :param refresh_token: JWT refresh token
        :return: tuple of (access_token, refresh_token, user_entity)
        """
        payload = self.token_service.decode_token(refresh_token, expected_type="refresh")
        subject = payload.get("sub")
        if not subject:
            raise InvalidTokenException("Missing token subject")

        user = self.user_repository.get_by_id(int(subject))
        if not user:
            raise UserNotFoundException(str(subject))

        if not user.is_active:
            raise UserInactiveException()

        new_access_token = self.token_service.create_access_token(
            subject=str(user.id),
            role=user.role,
            extra_claims={"email": user.email},
        )
        new_refresh_token = self.token_service.create_refresh_token(
            subject=str(user.id),
            role=user.role,
            extra_claims={"email": user.email},
        )

        return new_access_token, new_refresh_token, user

    def get_current_user(self, token: str) -> UserEntity:
        """
        Validate access token and return current user entity
        :param token: JWT access token
        :return: UserEntity
        """
        payload = self.token_service.decode_token(token, expected_type="access")
        subject = payload.get("sub")
        if not subject:
            raise InvalidTokenException("Missing token subject")

        user = self.user_repository.get_by_id(int(subject))
        if not user:
            raise UserNotFoundException(str(subject))

        if not user.is_active:
            raise UserInactiveException()

        return user
