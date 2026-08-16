from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.interface.schemas import CreateCountryRequest


def map_country_schema_to_entity(request: CreateCountryRequest) -> CountryEntity:
    return CountryEntity(
        name=request.name,
        country_code=request.country_code,
        currency_code=request.currency_code
    )