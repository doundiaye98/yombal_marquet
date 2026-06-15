# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import func

from extensions import db


class TimestampMixin:
    """Horodatage standard pour toutes les tables métier."""

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=func.now(),
    )
