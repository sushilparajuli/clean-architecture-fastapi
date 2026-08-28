from app.features.auth.domain.audit_log_entity import AuditLogEntity
from app.features.auth.infrastructure.models.audit_log_model import AuditLogModel


def map_audit_log_model_to_audit_log_entity(model: AuditLogModel) -> AuditLogEntity:
    """
    Map AuditLogModel to AuditLogEntity
    :arg model: AuditLogModel
    :return: AuditLogEntity
    """
    return AuditLogEntity(
        id=model.id,
        user_id=model.user_id,
        action=model.action,
        resource_type=model.resource_type,
        resource_id=model.resource_id,
        metadata=model.log_metadata,
        created_at=model.created_at,
    )
