from app.features.auth.domain.audit_log_entity import AuditLogEntity
from app.features.auth.infrastructure.models.audit_log_model import AuditLogModel


def map_audit_log_entity_to_audit_log_model(entity: AuditLogEntity) -> AuditLogModel:
    """
    Map AuditLogEntity to AuditLogModel
    :arg entity: AuditLogEntity
    :return: AuditLogModel
    """
    return AuditLogModel(
        id=entity.id,
        user_id=entity.user_id,
        action=entity.action,
        resource_type=entity.resource_type,
        resource_id=entity.resource_id,
        log_metadata=entity.metadata,
        created_at=entity.created_at,
    )
