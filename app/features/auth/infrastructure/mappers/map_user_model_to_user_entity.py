from app.features.auth.domain.user_entity import UserEntity
from app.features.auth.infrastructure.models.user_model import UserModel


def map_user_model_to_user_entity(model: UserModel) -> UserEntity:
    """
    Map UserModel to UserEntity
    :arg model: UserModel
    :return: UserEntity
    """
    return UserEntity(
        id=model.id,
        email=model.email,
        hashed_password=model.hashed_password,
        role=model.role,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
