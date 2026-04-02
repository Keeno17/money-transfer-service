from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit import AuditLog

import uuid


class AuditRepo:

    @staticmethod
    def get_by_id(session: Session, audit_id: uuid.UUID) -> AuditLog | None:
        stmt = select(AuditLog).where(AuditLog.id == audit_id)

        return session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all(session: Session) -> list[AuditLog]:
        return session.query(AuditLog).all()

    @staticmethod
    def create(session: Session, audit: AuditLog) -> AuditLog:
        session.add(audit)
        session.flush()
        session.refresh(audit)

    @staticmethod
    def update(session: Session, audit: AuditLog) -> AuditLog:
        session.flush()
        session.refresh(audit)
        return audit
