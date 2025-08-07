from datetime import datetime

from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class TimeStampMixin:
    created: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

