from abc import ABC, abstractmethod
from typing import Optional

from app.features.admin.country.domain.country_entity import CountryEntity


class ICountryRepository(ABC):
    """
    Interface for country repository
    """
    @abstractmethod
    def get_all_countries(self, skip: int, limit: int, search: Optional[str] = None) -> tuple[list[CountryEntity], int, int]:
        """
        Get all countries
        """
        pass

    @abstractmethod
    def get_country_by_id(self, country_id: int) -> CountryEntity:
        """
        Get country by id
        """
        pass

    @abstractmethod
    def create_country(self, country: CountryEntity) -> CountryEntity:
        """
        Create new country
        """
        pass

    @abstractmethod
    def update_country(self, country_id: int, country: CountryEntity) -> CountryEntity:
        """
        update country
        """
        pass

    @abstractmethod
    def delete_country(self, country_id: int) -> None:
        """
        delete a country
        """
        pass

