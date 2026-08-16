from dataclasses import dataclass
from datetime import  datetime
from typing import Optional


@dataclass
class CountryEntity:
    name: Optional[str] = None
    country_code: Optional[str] = None
    currency_code: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None