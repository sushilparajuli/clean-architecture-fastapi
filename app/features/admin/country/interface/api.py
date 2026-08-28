from typing import Annotated, Optional

from fastapi import Depends
from fastapi.params import Query
from starlette import status

from app.core.router.route import get_versioned_router
from app.features.admin.country.application.country_service import CountryService
from app.features.admin.country.infrastructure.mappers.map_country_schema_to_entity import (
    map_country_schema_to_entity,
)
from app.features.admin.country.infrastructure.mappers.map_country_update_schema_to_entity import (
    map_country_update_schema_to_entity,
)
from app.features.admin.country.interface.dependencies import get_country_service
from app.features.admin.country.interface.schemas import (
    CountryListResponse,
    CountryResponse,
    CreateCountryRequest,
    PaginationMeta,
    UpdateCountryRequest,
)
from app.features.auth.domain.user_entity import UserEntity
from app.features.auth.interface.dependencies import require_admin

v1_router = get_versioned_router("v1")


@v1_router.get(
    "/admin/countries",
    status_code=status.HTTP_200_OK,
    response_model=CountryListResponse,
)
@v1_router.get(
    "/admin/country",
    status_code=status.HTTP_200_OK,
    response_model=CountryListResponse,
    include_in_schema=False,
)
def get_countries(
    country_service: Annotated[CountryService, Depends(get_country_service)],
    skip: Annotated[
        int,
        Query(ge=1, description="Page number should be greater than or equal to 1"),
    ] = 1,
    limit: Annotated[
        int,
        Query(ge=1, description="Page size should be greater than or equal to 1"),
    ] = 10,
    search: Annotated[
        Optional[str], Query(description="Search query for country name")
    ] = None,
) -> CountryListResponse:
    """
    Get all countries
    :param search:
    :param skip:
    :param limit:
    :param country_service:
    :return: CountryListResponse
    """
    result, total, total_pages = country_service.get_all_countries(
        skip - 1, limit, search
    )
    meta: PaginationMeta = PaginationMeta(
        total=total,
        total_pages=total_pages,
        page_size=limit,
        current_page=skip,
    )
    return CountryListResponse(status="success", data=result, meta=meta)


@v1_router.get(
    "/admin/countries/{country_id}",
    status_code=status.HTTP_200_OK,
    response_model=CountryResponse,
)
@v1_router.get(
    "/admin/country/{country_id}",
    status_code=status.HTTP_200_OK,
    response_model=CountryResponse,
    include_in_schema=False,
)
def get_countries_by_id(
    country_id: int,
    country_service: Annotated[CountryService, Depends(get_country_service)],
) -> CountryResponse:
    """
    Get country by id
    :param country_id:
    :param country_service:
    :return: CountryResponse
    """
    result = country_service.get_by_id(country_id)
    return CountryResponse(status="success", data=result)


@v1_router.post(
    "/admin/countries",
    status_code=status.HTTP_201_CREATED,
    response_model=CountryResponse,
)
@v1_router.post(
    "/admin/country",
    status_code=status.HTTP_201_CREATED,
    response_model=CountryResponse,
    include_in_schema=False,
)
def create_country(
    data: CreateCountryRequest,
    country_service: Annotated[CountryService, Depends(get_country_service)],
    current_admin: Annotated[UserEntity, Depends(require_admin)],
) -> CountryResponse:
    data_entity = map_country_schema_to_entity(data)
    result = country_service.create_country(data_entity, actor=current_admin)
    return CountryResponse(status="success", data=result)


@v1_router.put(
    "/admin/countries/{country_id}",
    status_code=status.HTTP_200_OK,
    response_model=CountryResponse,
)
@v1_router.put(
    "/admin/country/{country_id}",
    status_code=status.HTTP_200_OK,
    response_model=CountryResponse,
    include_in_schema=False,
)
def put_country(
    country_id: int,
    data: UpdateCountryRequest,
    country_service: Annotated[CountryService, Depends(get_country_service)],
    current_admin: Annotated[UserEntity, Depends(require_admin)],
) -> CountryResponse:
    update_entity = map_country_update_schema_to_entity(data)
    result = country_service.update_country(
        country_id, update_entity, actor=current_admin
    )
    return CountryResponse(status="success", data=result)


@v1_router.patch(
    "/admin/countries/{country_id}",
    status_code=status.HTTP_200_OK,
    response_model=CountryResponse,
)
@v1_router.patch(
    "/admin/country/{country_id}",
    status_code=status.HTTP_200_OK,
    response_model=CountryResponse,
    include_in_schema=False,
)
@v1_router.patch(
    "/admin/countries",
    status_code=status.HTTP_200_OK,
    response_model=CountryResponse,
    include_in_schema=False,
)
def patch_country(
    data: UpdateCountryRequest,
    country_service: Annotated[CountryService, Depends(get_country_service)],
    current_admin: Annotated[UserEntity, Depends(require_admin)],
    country_id: Optional[int] = None,
) -> CountryResponse:
    target_id = country_id or (data.id if hasattr(data, "id") else None)
    if target_id is None:
        raise ValueError("country_id must be provided")
    update_entity = map_country_update_schema_to_entity(data)
    result = country_service.update_country(
        target_id, update_entity, actor=current_admin
    )
    return CountryResponse(status="success", data=result)


@v1_router.delete(
    "/admin/countries/{country_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@v1_router.delete(
    "/admin/country/{country_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
@v1_router.delete(
    "/admin/countries",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
def delete_country(
    country_service: Annotated[CountryService, Depends(get_country_service)],
    current_admin: Annotated[UserEntity, Depends(require_admin)],
    country_id: Optional[int] = None,
) -> None:
    if country_id is None:
        raise ValueError("country_id must be provided")
    country_service.delete_country(country_id, actor=current_admin)
