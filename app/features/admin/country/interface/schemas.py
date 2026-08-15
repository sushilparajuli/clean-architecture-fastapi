from http import HTTPStatus
from typing import List

from pydantic import BaseModel

from app.features.admin.country.domain.country_entity import CountryEntity


class CountryListResponse(BaseModel):
    status: str
    data: List[CountryEntity]


class CountryResponse(BaseModel):
    status: str
    data: CountryEntity

class DeleteResponse(BaseModel):
        status: str
        data: None
