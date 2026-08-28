class DomainException(Exception):
    pass

class NotFoundException(DomainException):
    pass

class AlreadyExistsException(DomainException):
    pass

class UnauthorizedException(DomainException):
    pass

class ForbiddenException(DomainException):
    pass
