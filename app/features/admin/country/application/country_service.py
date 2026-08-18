from typing import Optional

from app.core.exceptions.repository import UniqueConstraintFailure
from app.features.admin.country.application.interface.icountry_repository import ICountryRepository
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.domain.exceptions.exception import CountryAlreadyExistsException


class CountryService:
    def __init__(self, repository: ICountryRepository) -> None:
        self.repository = repository

    def get_all_countries(self, skip: int, limit: int, search: Optional[str] = None) -> tuple[list[CountryEntity], int, int]:
        """ Get all countries
        :return
            list[CountryEntity]: List of countries
        """
        return self.repository.get_all_countries(skip, limit, search)

    def get_by_id(self, country_id: int) -> CountryEntity:
        """ Get country by id
        :param country_id:
        :return: Country entity
        """
        return self.repository.get_country_by_id(country_id)

    def create_country(self, country_entity: CountryEntity) -> CountryEntity:
        try:
            """
            create a new country
            :param country_entity:
            :return: country entity
            """
            return self.repository.create_country(country_entity)
        except UniqueConstraintFailure:
            raise CountryAlreadyExistsException("Country", str(country_entity.name))

    def update_country(self, country_id: int, country_entity: CountryEntity) -> CountryEntity:
        try:
            """
            update a country
            :param country_id:
            :param country_entity:
            :return: country_entity
            """
            return self.repository.update_country(country_id, country_entity)
        except UniqueConstraintFailure:
            raise CountryAlreadyExistsException("Country", str(country_entity.id))

    def delete_country(self, country_id: int) -> None:
        """
        delete a country
        :param country_id:
        :return:
        """
        return self.repository.delete_country(country_id)

