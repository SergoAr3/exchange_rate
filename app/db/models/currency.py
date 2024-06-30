from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.config import Base


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(4), nullable=False, unique=True, index=True)

    exchange_rates_base = relationship("ExchangeRate", back_populates="base_currency",
                                       foreign_keys="[ExchangeRate.base_currency_id]")
    exchange_rates_target = relationship("ExchangeRate", back_populates="target_currency",
                                         foreign_keys="[ExchangeRate.target_currency_id]")

    def __str__(self):
        return f'{self.code}'
