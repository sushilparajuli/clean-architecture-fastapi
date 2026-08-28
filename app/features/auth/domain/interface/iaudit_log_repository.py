from abc import ABC, abstractmethod

from app.features.auth.domain.audit_log_entity import AuditLogEntity


class IAuditLogRepository(ABC):
    @abstractmethod
    def create_audit_log(self, audit_log: AuditLogEntity) -> AuditLogEntity:
        pass
