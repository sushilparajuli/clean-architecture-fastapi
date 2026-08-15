from typing import Annotated

from fastapi import Depends
from starlette import status

from app.core.router.route import get_versioned_router
from app.features.admin.country.application.country_service import CountryService
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.interface.dependencies import get_country_service
from app.features.admin.country.interface.schemas import CountryListResponse, CountryResponse, DeleteResponse

v1_router = get_versioned_router("v1")

@v1_router.get("/admin/countries")
def get_countries(
        country_service: Annotated[CountryService, Depends(get_country_service)],
) -> CountryListResponse:
    """
    Get all countries
    :param country_service:
    :return: CountryListResponse
    """
    result = country_service.get_all_countries()
    return CountryListResponse(status="success", data=result)

@v1_router.get("/admin/countries/{country_id}")
def get_countries_by_id(
        country_id: int,
        country_service: Annotated[CountryService, Depends(get_country_service)],
) -> CountryResponse:
    """
    Get all countries
    :param country_id:
    :param country_service:
    :return: CountryResponse
    """
    result = country_service.get_by_id(country_id)
    return CountryResponse(status="success", data=result)

@v1_router.post("/admin/countries")
def create_country(
        data: CountryEntity,
        country_service: Annotated[CountryService, Depends(get_country_service)],

)-> CountryResponse:
    result = country_service.create_country(data)
    return CountryResponse(status="success", data=result)

@v1_router.patch("/admin/countries")
def patch_country(
        country_id: int,
        data: CountryEntity,
        country_service: Annotated[CountryService, Depends(get_country_service)],

)-> CountryResponse:
    result = country_service.update_country(country_id,data)
    return CountryResponse(status="success", data=result)

@v1_router.delete("/admin/countries", status_code= status.HTTP_204_NO_CONTENT)
def delete_country(
        country_id: int,
        country_service: Annotated[CountryService, Depends(get_country_service)],

)-> None:
    country_service.delete_country(country_id)
