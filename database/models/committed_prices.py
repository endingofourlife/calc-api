from datetime import datetime

from sqlalchemy import Integer, Boolean, JSON, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base


class CommittedPrices(Base):
    __tablename__ = "committed_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reo_id: Mapped[int] = mapped_column(Integer, ForeignKey("real_estate_objects.id"), nullable=False)
    pricing_config_id: Mapped[int] = mapped_column(Integer, ForeignKey("pricing_configs.id"), nullable=False)
    distribution_config_id: Mapped[int] = mapped_column(Integer, ForeignKey("distribution_configs.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    actual_price: Mapped[float] = mapped_column(Float, nullable=False)
    x_rank: Mapped[float] = mapped_column(Float, nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Relationships
    real_estate_object: Mapped["RealEstateObject"] = relationship(back_populates="committed_prices")
    pricing_config: Mapped["PricingConfig"] = relationship(back_populates="committed_prices")
    distribution_config: Mapped["DistributionConfig"] = relationship(back_populates="committed_prices")

    __table_args__ = {
        "sqlite_autoincrement": True,
        "extend_existing": True
    }
