from typing import List

from sqlalchemy import Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.timestamp_mixin import TimeStampMixin


class PricingConfig(Base, TimeStampMixin):
    __tablename__ = "pricing_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    reo_id: Mapped[int] = mapped_column(Integer, ForeignKey("real_estate_objects.id"), nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Relationships
    real_estate_object: Mapped["RealEstateObject"] = relationship(back_populates="pricing_configs")
    committed_prices: Mapped[List["CommittedPrices"]] = relationship(back_populates="pricing_config")

    __table_args__ = {
        "sqlite_autoincrement": True,
        "extend_existing": True
    }