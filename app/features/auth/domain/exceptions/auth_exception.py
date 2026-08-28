from app.core.exceptions.domain import (
    DomainException,
    NotFoundException,
    AlreadyExistsException,
    UnauthorizedException,
    ForbiddenException,
)


class InvalidCredentialsException(UnauthorizedException):
    def __init__(self, message: str = "Invalid email or password"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenException(UnauthorizedException):
    def __init__(self, message: str = "Invalid or expired token"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(AlreadyExistsException):
    def __init__(self, email: str):
        self.message = f"User with email '{email}' already exists"
        super().__init__(self.message)


class UserNotFoundException(NotFoundException):
    def __init__(self, identifier: str):
        self.message = f"User '{identifier}' not found"
        super().__init__(self.message)


class UserInactiveException(ForbiddenException):
    def __init__(self, message: str = "User account is inactive"):
        self.message = message
        super().__init__(self.message)


class InsufficientPermissionsException(ForbiddenException):
    def __init__(self, message: str = "Admin privileges required"):
        self.message = message
        super().__init__(self.message)
