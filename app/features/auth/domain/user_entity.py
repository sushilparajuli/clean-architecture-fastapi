from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserEntity:
    id: Optional[int] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    role: str = "user"
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
