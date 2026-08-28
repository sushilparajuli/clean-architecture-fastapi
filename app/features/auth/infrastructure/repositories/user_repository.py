from typing import Optional, override
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions.repository import (
    ConnectionFailure,
    RepositoryException,
    TransactionFailure,
    UniqueConstraintFailure,
)
from app.features.auth.domain.interface.iuser_repository import IUserRepository
from app.features.auth.domain.user_entity import UserEntity
from app.features.auth.infrastructure.mappers.map_user_entity_to_user_model import (
    map_user_entity_to_user_model,
)
from app.features.auth.infrastructure.mappers.map_user_model_to_user_entity import (
    map_user_model_to_user_entity,
)
from app.features.auth.infrastructure.models.user_model import UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    @override
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        try:
            result = (
                self.session.query(UserModel).filter(UserModel.id == user_id).first()
            )
            if result is None:
                return None
            return map_user_model_to_user_entity(result)
        except OperationalError as e:
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            raise TransactionFailure() from e
        except Exception as e:
            raise RepositoryException() from e

    @override
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            result = (
                self.session.query(UserModel)
                .filter(UserModel.email == email.strip().lower())
                .first()
            )
            if result is None:
                return None
            return map_user_model_to_user_entity(result)
        except OperationalError as e:
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            raise TransactionFailure() from e
        except Exception as e:
            raise RepositoryException() from e

    @override
    def create_user(self, user: UserEntity) -> UserEntity:
        try:
            user_model = map_user_entity_to_user_model(user)
            if user_model.email:
                user_model.email = user_model.email.strip().lower()
            self.session.add(user_model)
            self.session.commit()
            self.session.refresh(user_model)
            return map_user_model_to_user_entity(user_model)
        except IntegrityError as e:
            self.session.rollback()
            raise UniqueConstraintFailure() from e
        except OperationalError as e:
            self.session.rollback()
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TransactionFailure() from e
        except Exception as e:
            self.session.rollback()
            raise RepositoryException() from e

    @override
    def update_user(self, user_id: int, user: UserEntity) -> UserEntity:
        try:
            user_model = (
                self.session.query(UserModel).filter(UserModel.id == user_id).first()
            )
            if not user_model:
                raise ValueError(f"User with ID {user_id} not found")

            user_data = user.__dict__
            for key, value in user_data.items():
                if value is not None and hasattr(user_model, key) and key != "id":
                    if key == "email" and isinstance(value, str):
                        value = value.strip().lower()
                    setattr(user_model, key, value)

            self.session.commit()
            self.session.refresh(user_model)
            return map_user_model_to_user_entity(user_model)
        except IntegrityError as e:
            self.session.rollback()
            raise UniqueConstraintFailure() from e
        except OperationalError as e:
            self.session.rollback()
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TransactionFailure() from e
        except Exception as e:
            self.session.rollback()
            raise RepositoryException() from e
