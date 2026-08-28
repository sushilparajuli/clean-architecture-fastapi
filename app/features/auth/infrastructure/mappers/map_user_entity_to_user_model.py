from app.features.auth.domain.user_entity import UserEntity
from app.features.auth.infrastructure.models.user_model import UserModel


def map_user_entity_to_user_model(entity: UserEntity) -> UserModel:
    """
    Map UserEntity to UserModel
    :arg entity: UserEntity
    :return: UserModel
    """
    return UserModel(
        id=entity.id,
        email=entity.email,
        hashed_password=entity.hashed_password,
        role=entity.role,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
