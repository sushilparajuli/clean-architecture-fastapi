from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.providers.db import get_db_session
from app.features.admin.country.application.country_service import CountryService
from app.features.admin.country.application.interface.icountry_repository import ICountryRepository
from app.features.admin.country.infrastructure.repositories.country_repository import CountryRepository


def get_country_repository(
        db_session: Annotated[Session, Depends(get_db_session)]
) -> ICountryRepository:
    """
    Get country repository
    :param db_session:
    :return: ICountryRepository
    """
    return CountryRepository(session=db_session)

def get_country_service(country_repository: Annotated[ICountryRepository, Depends(get_country_repository)]) -> CountryService:
    """
    Get country service
    :param country_repository:
    :return: CountryService
    """
    return CountryService(country_repository)