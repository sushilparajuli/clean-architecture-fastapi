from http import HTTPStatus
from typing import List, Optional

from pydantic import BaseModel

from app.features.admin.country.domain.country_entity import CountryEntity


class CreateCountryRequest(BaseModel):
    name: str
    country_code: str
    currency_code: str

class PaginationMeta(BaseModel):
    total: int
    total_pages: int
    page_size: int
    current_page: int


class UpdateCountryRequest(BaseModel):
    name: Optional[str] = None
    country_code: Optional[str] = None
    currency_code: Optional[str] = None

class CountryListResponse(BaseModel):
    status: str
    data: List[CountryEntity]
    meta: PaginationMeta


class CountryResponse(BaseModel):
    status: str
    data: CountryEntity

class DeleteResponse(BaseModel):
        status: str
        data: None
