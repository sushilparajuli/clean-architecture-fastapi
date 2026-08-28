from typing import override
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions.repository import (
    ConnectionFailure,
    RepositoryException,
    TransactionFailure,
)
from app.features.auth.domain.audit_log_entity import AuditLogEntity
from app.features.auth.domain.interface.iaudit_log_repository import (
    IAuditLogRepository,
)
from app.features.auth.infrastructure.mappers.map_audit_log_entity_to_audit_log_model import (
    map_audit_log_entity_to_audit_log_model,
)
from app.features.auth.infrastructure.mappers.map_audit_log_model_to_audit_log_entity import (
    map_audit_log_model_to_audit_log_entity,
)


class AuditLogRepository(IAuditLogRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    @override
    def create_audit_log(self, audit_log: AuditLogEntity) -> AuditLogEntity:
        try:
            model = map_audit_log_entity_to_audit_log_model(audit_log)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return map_audit_log_model_to_audit_log_entity(model)
        except OperationalError as e:
            self.session.rollback()
            raise ConnectionFailure() from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TransactionFailure() from e
        except Exception as e:
            self.session.rollback()
            raise RepositoryException() from e
