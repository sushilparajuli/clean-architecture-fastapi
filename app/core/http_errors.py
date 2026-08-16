from urllib.request import Request

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.exceptions.repository import RepositoryException, ConnectionFailure, TransactionFailure, \
    UniqueConstraintFailure


def register_http_error_handler(app: FastAPI):
   """
    Register HTTP error handlers for the given FastAPI application.

    :param app: The FastAPI application to register the error handlers for.
    :return: JSON Response with error details.
   """
   @app.exception_handler(RepositoryException)
   async def handle_repository_exception(req: Request, exception:RepositoryException):
       if isinstance(exception, ConnectionFailure):
           code= "DB_CONNECTION_FAILURE"
       elif isinstance(exception, TransactionFailure):
            code = "DB_TRANSACTION_FAILURE"
       elif isinstance(exception, UniqueConstraintFailure):
            code = "DB_UNIQUE_CONSTRAINT_FAILURE"
       else:
           code = "DB_UNKNOWN_FAILURE"

       return JSONResponse(
           status_code=503,
           content={
               "code": code,
               "message": "Database service temporary unavailable",
               "detail": str(exception)
           }
       )