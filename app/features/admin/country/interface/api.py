from typing import Annotated, Optional

from fastapi import Depends
from fastapi.params import Query
from starlette import status

from app.core.router.route import get_versioned_router
from app.features.admin.country.application.country_service import CountryService
from app.features.admin.country.domain.country_entity import CountryEntity
from app.features.admin.country.infrastructure.mappers.map_country_schema_to_entity import map_country_schema_to_entity
from app.features.admin.country.infrastructure.mappers.map_country_update_schema_to_entity import map_country_update_schema_to_entity
from app.features.admin.country.interface.dependencies import get_country_service
from app.features.admin.country.interface.schemas import CountryListResponse, CountryResponse, DeleteResponse, \
    CreateCountryRequest, UpdateCountryRequest, PaginationMeta

v1_router = get_versioned_router("v1")

@v1_router.get("/admin/countries")
def get_countries(
        country_service: Annotated[CountryService, Depends(get_country_service)],
        skip: Annotated[int, Query(ge=1, description="Page number should be be greater than or equal to 1")],
        limit: Annotated[int, Query(ge=1, description="Page size should be be greater than or equal to 1")],
        search: Annotated[Optional[str], Query(description="Search query for country name ")] = None
) -> CountryListResponse:
    """
    Get all countries
    :param search:
    :param skip:
    :param limit:
    :param country_service:
    :return: CountryListResponse
    """
    result, total, total_pages = country_service.get_all_countries(skip-1, limit,search)
    meta : PaginationMeta = PaginationMeta(
        total=total,
        total_pages=total_pages,
        page_size=limit,
        current_page=skip)
    return CountryListResponse(status="success", data=result, meta=meta)

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
        data: CreateCountryRequest,
        country_service: Annotated[CountryService, Depends(get_country_service)],

)-> CountryResponse:
    data_entity = map_country_schema_to_entity(data)
    result = country_service.create_country(data_entity)
    return CountryResponse(status="success", data=result)




@v1_router.patch("/admin/countries")
def patch_country(
        country_id: int,
        data: UpdateCountryRequest,
        country_service: Annotated[CountryService, Depends(get_country_service)],

)-> CountryResponse:
    update_entity = map_country_update_schema_to_entity(data)
    result = country_service.update_country(country_id,update_entity)
    return CountryResponse(status="success", data=result)

@v1_router.delete("/admin/countries", status_code= status.HTTP_204_NO_CONTENT)
def delete_country(
        country_id: int,
        country_service: Annotated[CountryService, Depends(get_country_service)],

)-> None:
    country_service.delete_country(country_id)
