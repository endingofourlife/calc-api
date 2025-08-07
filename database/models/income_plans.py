from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base


class IncomePlan(Base):
    __tablename__ = "income_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    reo_id: Mapped[int] = mapped_column(Integer, ForeignKey("real_estate_objects.id"), nullable=False)
    property_type: Mapped[str] = mapped_column(String, nullable=False)
    period_begin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    area: Mapped[float] = mapped_column(Float, nullable=False)
    planned_sales_revenue: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_sqm: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_sqm_end: Mapped[float] = mapped_column(Float, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    real_estate_object: Mapped["RealEstateObject"] = relationship(back_populates="income_plans")

    __table_args__ = {
        "sqlite_autoincrement": True,
        "extend_existing": True
    }