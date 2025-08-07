from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class StatusMapping(Base):
    __tablename__ = "status_mappings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reo_id: Mapped[int] = mapped_column(Integer, ForeignKey("real_estate_objects.id"), nullable=False)
    dev_status: Mapped[str] = mapped_column(String, nullable=False)
    sys_status: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    real_estate_object: Mapped["RealEstateObject"] = relationship(back_populates="status_mappings")

    __table_args__ = {
        "sqlite_autoincrement": True,
        "extend_existing": True
    }