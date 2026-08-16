class RepositoryException(Exception):
    pass

class ConnectionFailure(RepositoryException):
    pass


class TransactionFailure(RepositoryException):
    pass

class UniqueConstraintFailure(RepositoryException):
    pass