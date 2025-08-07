from typing import Optional, List

from sqlalchemy import Integer, String, Float, Boolean, JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from .mixins.timestamp_mixin import TimeStampMixin


class RealEstateObject(Base, TimeStampMixin):
    __tablename__ = "real_estate_objects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lon: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    curr: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    custom_fields: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    premises: Mapped[List["Premises"]] = relationship(back_populates="real_estate_object")
    pricing_configs: Mapped[List["PricingConfig"]] = relationship(back_populates="real_estate_object")
    committed_prices: Mapped[List["CommittedPrices"]] = relationship(back_populates="real_estate_object")
    income_plans: Mapped[List["IncomePlan"]] = relationship(back_populates="real_estate_object")
    status_mappings: Mapped[List["StatusMapping"]] = relationship(back_populates="real_estate_object")

    __table_args__ = {
        "sqlite_autoincrement": True,
        "extend_existing": True
    }
