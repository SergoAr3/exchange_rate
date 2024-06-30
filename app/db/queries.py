from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import aliased

from app.db.models.exchange_rate import ExchangeRate
from app.db.models.currency import Currency
from app.db.config import Database

load_dotenv()

async_session = Database().session


class CurrencyTable:
    def __init__(self):
        self.session = async_session

    async def save_currency(self, currency_code: str) -> None:
        async with self.session() as session:
            async with session.begin():
                currency_id = await session.execute(select(Currency.id).where(Currency.code == currency_code))
                currency_id = currency_id.scalars().first()
                if not currency_id:
                    session.add(Currency(code=currency_code))

    async def get_currency_id(self, currency_code: str) -> int:
        async with self.session() as session:
            async with session.begin():
                currency_id = await session.execute(select(Currency.id).where(Currency.code == currency_code))
                currency_id = currency_id.scalars().first()

                return currency_id


class ExchangeRateTable:
    def __init__(self):
        self.session = async_session

    async def save_exchange_rate(self, base_currency: int, target_currency: int, rate: float) -> None:
        async with self.session() as session:
            async with session.begin():
                session.add(ExchangeRate(base_currency_id=base_currency, target_currency_id=target_currency, rate=rate))

    async def get_exchange_rate(self, base_currency: str, target_currency: str) -> float:
        async with self.session() as session:
            async with session.begin():
                base_currency_alias = aliased(Currency)
                target_currency_alias = aliased(Currency)

                rate = await session.execute(
                    select(ExchangeRate.rate)
                    .join(base_currency_alias, ExchangeRate.base_currency_id == base_currency_alias.id)
                    .join(target_currency_alias, ExchangeRate.target_currency_id == target_currency_alias.id)
                    .where(base_currency_alias.code == base_currency)
                    .where(target_currency_alias.code == target_currency)
                )

                rate = rate.scalars().first()
                return rate

    async def currency_conversion(self, base_currency: str, target_currency: str, amount) -> float | None:
        rate = await self.get_exchange_rate(base_currency, target_currency)
        if rate:
            return amount * rate
        return None


exchange_rate_table = ExchangeRateTable()
currency_table = CurrencyTable()
