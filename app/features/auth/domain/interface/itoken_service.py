from abc import ABC, abstractmethod
from typing import Any, Optional


class ITokenService(ABC):
    @abstractmethod
    def create_access_token(self, subject: str, role: str, extra_claims: Optional[dict[str, Any]] = None) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, subject: str, role: str, extra_claims: Optional[dict[str, Any]] = None) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str, expected_type: Optional[str] = None) -> dict[str, Any]:
        pass
