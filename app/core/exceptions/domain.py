class DomainException(Exception):
    pass

class NotFoundException(DomainException):
    pass

class AlreadyExistsException(DomainException):
    pass
