from typing import override
import math
from sqlalchemy.orm import Session

from app.features.admin.country.application.interface.icountry_repository import ICountryRepository
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.infrastructure.mappers.map_country_model_to_country_entity import map_country_model_to_country_entity
from app.features.admin.country.infrastructure.mappers.map_country_entity_to_country_model import \
    map_country_entity_to_country_model
from app.features.admin.country.infrastructure.models import country_model
from app.features.admin.country.infrastructure.models.country_model import CountryModel


class CountryRepository(ICountryRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    @override
    def get_all_countries(self, skip: int, limit: int) -> tuple[list[CountryEntity], int, int]:
        """
        get all countries
        return:
         list[CountryEntity]: List of countries
        """
        countries =  self.session.query(CountryModel).offset(skip).limit(limit).all()

        # count all the records by id
        total = self.session.query(CountryModel.id).scalar() or 0
        total_pages = math.ceil(total / limit) if limit > 0 else 1
        # Map country model to country entity
        result = [map_country_model_to_country_entity(country) for country in countries]
        return result, total, total_pages

    @override
    def get_country_by_id(self, country_id: int) -> CountryEntity:
        """
        Get country by id
        arg:
         country_id (int): Country id
        return:
         CountryEntity: Country entity
        """
        result: CountryModel | None = self.session.query(CountryModel).filter(CountryModel.id == country_id).first()
        if result is None:
            raise ValueError(f"Country with ID {country_id} not found")
        return  map_country_model_to_country_entity(result)

    @override
    def create_country(self, country: CountryEntity):
        """
        Create new country
        arg:
            country (CountryEntity): Country entity
        return
            None
        """
        result = map_country_entity_to_country_model(country)
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return map_country_model_to_country_entity(result)

    @override
    def update_country(self, country_id:int, country: CountryEntity):
        """
        Update country
        arg:
            country (CountryEntity): Country entity
        return
            CountryEntity: Country entity
        """
        result = self.session.query(CountryModel).filter(CountryModel.id == country_id).first()
        if not result:
            raise ValueError(f"Country with ID {country_id} not found")

        country_data = country.__dict__
        # 3. Dynamic patch update: loop through attributes and set valid values
        for key, value in country_data.items():
            # Update only provided/non-None fields, match DB schema, and protect the primary key
            if value is not None and hasattr(result, key) and key != 'id':
                setattr(result, key, value)
        # 3. Commit changes (SQLAlchemy auto-tracks modifications to country_model)
        self.session.commit()
        self.session.refresh(result)

        return map_country_model_to_country_entity(result)

    @override
    def delete_country(self, country_id:int) -> None:
        """
        Delete country
        arg:
           country_id (int): Country id
        :return
        None
        """
        data = self.session.query(CountryModel).filter(CountryModel.id == country_id).first()
        if not data:
            raise ValueError(f"Country with ID {country_id} not found")
        self.session.delete(data)
        self.session.commit()
        return None
