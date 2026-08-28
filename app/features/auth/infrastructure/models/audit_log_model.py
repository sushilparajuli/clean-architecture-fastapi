from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, func

from app.core.data.source.local.base import Base


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    log_metadata = Column("metadata", JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
