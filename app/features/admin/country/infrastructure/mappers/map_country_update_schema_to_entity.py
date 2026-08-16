from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.interface.schemas import UpdateCountryRequest


def map_country_update_schema_to_entity(request: UpdateCountryRequest) -> CountryEntity:
    return CountryEntity(
        name=request.name,
        country_code=request.country_code,
        currency_code=request.currency_code
    )
