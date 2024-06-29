from dotenv import load_dotenv

from sqlalchemy import String, ForeignKey, Float, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

load_dotenv()


class Base(DeclarativeBase):
    pass


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(4), nullable=False, unique=True, index=True)

    exchange_rates_base: Mapped["ExchangeRate"] = relationship("ExchangeRate", back_populates="base_currency",
                                                               foreign_keys="[ExchangeRate.base_currency_id]")
    exchange_rates_target: Mapped["ExchangeRate"] = relationship("ExchangeRate", back_populates="target_currency",
                                                                 foreign_keys="[ExchangeRate.target_currency_id]")

    def __str__(self):
        return f'{self.code}'


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'), nullable=False,
                                                  index=True)
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete='CASCADE'), nullable=False,
                                                    index=True)
    rate: Mapped[float] = mapped_column(Float, nullable=False)

    base_currency: Mapped[Currency] = relationship("Currency", foreign_keys=[base_currency_id],
                                                   back_populates="exchange_rates_base")
    target_currency: Mapped[Currency] = relationship("Currency", foreign_keys=[target_currency_id],
                                                     back_populates="exchange_rates_target")

    __table_args__ = (
        Index('base_target_id_index', 'base_currency_id', 'target_currency_id'),
    )