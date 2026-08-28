from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.providers.db import get_db_session
from app.features.admin.country.application.country_service import CountryService
from app.features.admin.country.application.interface.icountry_repository import ICountryRepository
from app.features.admin.country.infrastructure.repositories.country_repository import CountryRepository
from app.features.auth.domain.interface.iaudit_log_repository import IAuditLogRepository
from app.features.auth.interface.dependencies import get_audit_log_repository


def get_country_repository(
        db_session: Annotated[Session, Depends(get_db_session)]
) -> ICountryRepository:
    """
    Get country repository
    :param db_session:
    :return: ICountryRepository
    """
    return CountryRepository(session=db_session)

def get_country_service(
    country_repository: Annotated[ICountryRepository, Depends(get_country_repository)],
    audit_log_repository: Annotated[IAuditLogRepository, Depends(get_audit_log_repository)],
) -> CountryService:
    """
    Get country service
    :param country_repository:
    :param audit_log_repository:
    :return: CountryService
    """
    return CountryService(
        repository=country_repository,
        audit_log_repository=audit_log_repository,
    )