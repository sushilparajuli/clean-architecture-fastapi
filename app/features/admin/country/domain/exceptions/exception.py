from app.core.exceptions.domain import NotFoundException, AlreadyExistsException


class CountryNotFoundException(NotFoundException):
    def __init__(self, entity: str, key:str):
        message = f"{entity} not found with key {key}"
        self.message = message

        super().__init__(message)


class CountryAlreadyExistsException(AlreadyExistsException):
    def __init__(self, entity: str, key:str):
        message = f"{entity} already exists with key {key}"
        self.message = message

        super().__init__(message)