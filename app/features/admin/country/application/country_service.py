from typing import Optional

from app.core.exceptions.repository import UniqueConstraintFailure
from app.features.admin.country.application.interface.icountry_repository import ICountryRepository
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.domain.exceptions.exception import CountryAlreadyExistsException
from app.features.auth.domain.audit_log_entity import AuditLogEntity
from app.features.auth.domain.interface.iaudit_log_repository import IAuditLogRepository
from app.features.auth.domain.user_entity import UserEntity


class CountryService:
    def __init__(
        self,
        repository: ICountryRepository,
        audit_log_repository: Optional[IAuditLogRepository] = None,
    ) -> None:
        self.repository = repository
        self.audit_log_repository = audit_log_repository

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

    def create_country(
        self,
        country_entity: CountryEntity,
        actor: Optional[UserEntity] = None,
    ) -> CountryEntity:
        try:
            """
            create a new country
            :param country_entity:
            :param actor:
            :return: country entity
            """
            result = self.repository.create_country(country_entity)
            if self.audit_log_repository:
                self.audit_log_repository.create_audit_log(
                    AuditLogEntity(
                        user_id=actor.id if actor else None,
                        action="COUNTRY_CREATE",
                        resource_type="country",
                        resource_id=str(result.id) if result.id is not None else None,
                        metadata={
                            "name": result.name,
                            "country_code": result.country_code,
                            "currency_code": result.currency_code,
                        },
                    )
                )
            return result
        except UniqueConstraintFailure:
            raise CountryAlreadyExistsException("Country", str(country_entity.name))

    def update_country(
        self,
        country_id: int,
        country_entity: CountryEntity,
        actor: Optional[UserEntity] = None,
    ) -> CountryEntity:
        try:
            """
            update a country
            :param country_id:
            :param country_entity:
            :param actor:
            :return: country_entity
            """
            result = self.repository.update_country(country_id, country_entity)
            if self.audit_log_repository:
                updated_fields = {
                    k: v
                    for k, v in country_entity.__dict__.items()
                    if v is not None and k != "id"
                }
                self.audit_log_repository.create_audit_log(
                    AuditLogEntity(
                        user_id=actor.id if actor else None,
                        action="COUNTRY_UPDATE",
                        resource_type="country",
                        resource_id=str(country_id),
                        metadata={
                            "id": country_id,
                            "updated_fields": updated_fields,
                            "name": result.name,
                            "country_code": result.country_code,
                            "currency_code": result.currency_code,
                        },
                    )
                )
            return result
        except UniqueConstraintFailure:
            raise CountryAlreadyExistsException("Country", str(country_entity.id))

    def delete_country(
        self,
        country_id: int,
        actor: Optional[UserEntity] = None,
    ) -> None:
        """
        delete a country
        :param country_id:
        :param actor:
        :return:
        """
        result = self.repository.delete_country(country_id)
        if self.audit_log_repository:
            self.audit_log_repository.create_audit_log(
                AuditLogEntity(
                    user_id=actor.id if actor else None,
                    action="COUNTRY_DELETE",
                    resource_type="country",
                    resource_id=str(country_id),
                    metadata={"country_id": country_id},
                )
            )
        return result

