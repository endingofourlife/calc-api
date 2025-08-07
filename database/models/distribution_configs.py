from typing import List

from sqlalchemy import Integer, String, Boolean, JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base


class DistributionConfig(Base):
    __tablename__ = "distribution_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    func_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    committed_prices: Mapped[List["CommittedPrices"]] = relationship(back_populates="distribution_config")

    __table_args__ = {
        "sqlite_autoincrement": True,
        "extend_existing": True
    }
