from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import select

from dependency_injector import containers, providers

from models import Currency, ExchangeRate


class Database:
    def __init__(self, engine: create_engine, session: sessionmaker):
        self.engine = engine
        self.session = session


class CurrencyTable:
    def __init__(self, session: sessionmaker):
        self.session = session

    def save_currency(self, currency_code: str) -> None:
        with self.session() as session:
            with session.begin():
                currency_id = session.execute(select(Currency.id).where(Currency.code == currency_code)).scalar()
                if not currency_id:
                    session.add(Currency(code=currency_code))

    def get_currency_id(self, currency_code: str) -> int:
        with self.session() as session:
            with session.begin():
                currency_id = session.execute(select(Currency.id).where(Currency.code == currency_code)).scalar()

                return currency_id


class ExchangeRateTable:
    def __init__(self, session: sessionmaker):
        self.session = session

    def save_exchange_rate(self, base_currency: int, target_currency: int, rate: float) -> None:
        with self.session() as session:
            with session.begin():
                session.add(ExchangeRate(base_currency_id=base_currency, target_currency_id=target_currency, rate=rate))

    def get_exchange_rate(self, base_currency: str, target_currency: str) -> float:
        with self.session() as session:
            with session.begin():
                base_currency_alias = aliased(Currency)
                target_currency_alias = aliased(Currency)

                rate = session.execute(
                    select(ExchangeRate.rate)
                    .join(base_currency_alias, ExchangeRate.base_currency_id == base_currency_alias.id)
                    .join(target_currency_alias, ExchangeRate.target_currency_id == target_currency_alias.id)
                    .where(base_currency_alias.code == base_currency)
                    .where(target_currency_alias.code == target_currency)
                ).scalar()

                return rate

    def currency_conversion(self, base_currency: str, target_currency: str, amount) -> float | None:
        rate = self.get_exchange_rate(base_currency, target_currency)
        if rate:
            return amount * rate
        return None


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Singleton(
        create_engine,
        config.database.database_url,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True
    )
    session = providers.Singleton(
        sessionmaker,
        bind=engine,
        expire_on_commit=False
    )

    database = providers.Singleton(
        Database,
        engine=engine,
        session=session
    )

    currency_table = providers.Factory(
        CurrencyTable,
        session=database.provided.session
    )
    exchange_rate_table = providers.Factory(
        ExchangeRateTable,
        session=database.provided.session
    )
