from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class AuditLogEntity:
    id: Optional[int] = None
    user_id: Optional[int] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    created_at: Optional[datetime] = None
