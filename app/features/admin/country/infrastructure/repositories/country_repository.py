from typing import override, Optional
import math

from sqlalchemy import or_, func
from sqlalchemy.exc import OperationalError, SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session


from app.core.exceptions.repository import ConnectionFailure, TransactionFailure, RepositoryException, \
    UniqueConstraintFailure
from app.features.admin.country.application.interface.icountry_repository import ICountryRepository
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.domain.exceptions.exception import CountryNotFoundException
from app.features.admin.country.infrastructure.mappers.map_country_model_to_country_entity import map_country_model_to_country_entity
from app.features.admin.country.infrastructure.mappers.map_country_entity_to_country_model import \
    map_country_entity_to_country_model
from app.features.admin.country.infrastructure.models import country_model
from app.features.admin.country.infrastructure.models.country_model import CountryModel


class CountryRepository(ICountryRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    @override
    def get_all_countries(self, skip: int, limit: int, search: Optional[str] = None) -> tuple[list[CountryEntity], int, int]:
        try:
            """
            get all countries
            return:
             list[CountryEntity]: List of countries
            """
            #base query
            query = self.session.query(CountryModel)
            #search by name, country_code, currency_code
            if search:
                pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        CountryModel.name.ilike(pattern),
                        CountryModel.country_code.ilike(pattern),
                        CountryModel.currency_code.ilike(pattern)
                    )
                )
            # self.session.query(CountryModel).offset(skip).limit(limit).all()

            # sort by the name in asc, then paginate
            countries = (
                query.order_by(CountryModel.name.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            # count all the records by id
            total = query.with_entities(func.count(CountryModel.id)).scalar() or 0
            total_pages = math.ceil(total / limit) if limit > 0 else 1
            # Map country model to country entity
            result = [map_country_model_to_country_entity(country) for country in countries]
            return result, total, total_pages
        except OperationalError as e:
                raise ConnectionFailure() from e
        except SQLAlchemyError as e:
                raise TransactionFailure() from e
        except Exception as e:
                raise RepositoryException() from e

    @override
    def get_country_by_id(self, country_id: int) -> CountryEntity:
        try:
            """
            Get country by id
            arg:
             country_id (int): Country id
            return:
             CountryEntity: Country entity
            """
            result: CountryModel | None = self.session.query(CountryModel).filter(CountryModel.id == country_id).first()
            if result is None:
                raise CountryNotFoundException("Country", str(country_id))
            return  map_country_model_to_country_entity(result)
        except OperationalError as e:
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            raise TransactionFailure() from e

    @override
    def create_country(self, country: CountryEntity):
        try:
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
        except IntegrityError as e:
            self.session.rollback()
            raise UniqueConstraintFailure() from e
        except OperationalError as e:
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            raise TransactionFailure() from e
        except Exception as e:
            raise RepositoryException() from e
    @override
    def update_country(self, country_id:int, country: CountryEntity):
        try:
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
        except IntegrityError as e:
            self.session.rollback()
            raise UniqueConstraintFailure() from e
        except OperationalError as e:
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            raise TransactionFailure() from e
        except Exception as e:
            raise RepositoryException() from e

    @override
    def delete_country(self, country_id:int) -> None:
        try:
            """
            Delete country
            arg:
               country_id (int): Country id
            :return
            None
            """
            data = self.session.query(CountryModel).filter(CountryModel.id == country_id).first()
            if not data:
                raise CountryNotFoundException("Country", str(country_id))
            self.session.delete(data)
            self.session.commit()
            return None
        except OperationalError as e:
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            raise TransactionFailure() from e
