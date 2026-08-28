from abc import ABC, abstractmethod
from typing import Optional

from app.features.auth.domain.user_entity import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user: UserEntity) -> UserEntity:
        pass
