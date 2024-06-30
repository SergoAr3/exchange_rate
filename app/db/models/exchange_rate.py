from sqlalchemy import ForeignKey, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.config import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'), nullable=False,
                                                  index=True)
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'), nullable=False,
                                                    index=True)
    rate: Mapped[float] = mapped_column(Float, nullable=False)

    base_currency = relationship("Currency", foreign_keys=[base_currency_id],
                                 back_populates="exchange_rates_base")
    target_currency = relationship("Currency", foreign_keys=[target_currency_id],
                                   back_populates="exchange_rates_target")

    __table_args__ = (
        Index('base_target_id_index', 'base_currency_id', 'target_currency_id'),
    )
