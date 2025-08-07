from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base


class Sales(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    premises_id: Mapped[int] = mapped_column(Integer, ForeignKey("premises.id"), nullable=False)
    saledate: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    premises: Mapped["Premises"] = relationship(back_populates="sales")

    __table_args__ = {
        "sqlite_autoincrement": True,
        "extend_existing": True
    }