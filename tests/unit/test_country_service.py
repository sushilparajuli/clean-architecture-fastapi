from typing import Optional, override
import pytest

from app.features.admin.country.application.country_service import CountryService
from app.features.admin.country.application.interface.icountry_repository import (
    ICountryRepository,
)
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.auth.domain.audit_log_entity import AuditLogEntity
from app.features.auth.domain.interface.iaudit_log_repository import (
    IAuditLogRepository,
)
from app.features.auth.domain.user_entity import UserEntity


class InMemoryCountryRepository(ICountryRepository):
    def __init__(self):
        self.countries: dict[int, CountryEntity] = {}
        self.counter = 1

    @override
    def get_all_countries(
        self, skip: int, limit: int, search: Optional[str] = None
    ) -> tuple[list[CountryEntity], int, int]:
        items = list(self.countries.values())
        return items[skip : skip + limit], len(items), 1

    @override
    def get_country_by_id(self, country_id: int) -> CountryEntity:
        return self.countries[country_id]

    @override
    def create_country(self, country: CountryEntity) -> CountryEntity:
        c_id = self.counter
        self.counter += 1
        created = CountryEntity(
            id=c_id,
            name=country.name,
            country_code=country.country_code,
            currency_code=country.currency_code,
        )
        self.countries[c_id] = created
        return created

    @override
    def update_country(
        self, country_id: int, country: CountryEntity
    ) -> CountryEntity:
        current = self.countries[country_id]
        if country.name:
            current.name = country.name
        if country.country_code:
            current.country_code = country.country_code
        if country.currency_code:
            current.currency_code = country.currency_code
        return current

    @override
    def delete_country(self, country_id: int) -> None:
        self.countries.pop(country_id, None)


class InMemoryAuditLogRepository(IAuditLogRepository):
    def __init__(self):
        self.logs: list[AuditLogEntity] = []

    @override
    def create_audit_log(self, audit_log: AuditLogEntity) -> AuditLogEntity:
        self.logs.append(audit_log)
        return audit_log


def test_country_service_with_audit_logs():
    country_repo = InMemoryCountryRepository()
    audit_repo = InMemoryAuditLogRepository()
    service = CountryService(
        repository=country_repo, audit_log_repository=audit_repo
    )
    admin = UserEntity(id=42, email="admin@test.com", role="admin")

    # 1. Create
    created = service.create_country(
        CountryEntity(name="Nepal", country_code="NP", currency_code="NPR"),
        actor=admin,
    )
    assert created.id is not None
    assert len(audit_repo.logs) == 1
    assert audit_repo.logs[0].action == "COUNTRY_CREATE"
    assert audit_repo.logs[0].user_id == 42
    assert audit_repo.logs[0].resource_id == str(created.id)

    # 2. Update
    updated = service.update_country(
        created.id,
        CountryEntity(currency_code="USD"),
        actor=admin,
    )
    assert len(audit_repo.logs) == 2
    assert audit_repo.logs[1].action == "COUNTRY_UPDATE"
    assert audit_repo.logs[1].user_id == 42
    assert audit_repo.logs[1].resource_id == str(created.id)

    # 3. Delete
    service.delete_country(created.id, actor=admin)
    assert len(audit_repo.logs) == 3
    assert audit_repo.logs[2].action == "COUNTRY_DELETE"
    assert audit_repo.logs[2].user_id == 42
