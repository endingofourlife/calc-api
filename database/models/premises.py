from datetime import datetime
from typing import Optional, List

from sqlalchemy import Integer, String, Float, Boolean, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from .mixins.timestamp_mixin import TimeStampMixin


class Premises(Base, TimeStampMixin):
    __tablename__ = "premises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reo_id: Mapped[int] = mapped_column(Integer, ForeignKey("real_estate_objects.id"), nullable=False)
    uploaded: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    property_type: Mapped[str] = mapped_column(String, nullable=False)
    premises_id: Mapped[str] = mapped_column(String, nullable=False)
    number_of_unit: Mapped[int] = mapped_column(Integer, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    entrance: Mapped[str] = mapped_column(String, nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    layout_type: Mapped[str] = mapped_column(String, nullable=False)
    full_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_area_m2: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_area_m2: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_meter: Mapped[float] = mapped_column(Float, nullable=False)
    number_of_rooms: Mapped[int] = mapped_column(Integer, nullable=False)
    living_area_m2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    kitchen_area_m2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    view_from_window: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    number_of_levels: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    number_of_loggias: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    number_of_balconies: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    number_of_bathrooms_with_toilets: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    number_of_separate_bathrooms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    number_of_terraces: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    studio: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    sales_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    customcontent: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    real_estate_object: Mapped["RealEstateObject"] = relationship(back_populates="premises")
    sales: Mapped[List["Sales"]] = relationship(back_populates="premises")

    __table_args__ = {
        "sqlite_autoincrement": True,
        "extend_existing": True
    }