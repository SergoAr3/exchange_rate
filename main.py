import sys

import requests
import os

from dotenv import load_dotenv

from fastapi import Depends, FastAPI

from dependency_injector.wiring import Provide, inject

from models import Base
from services import Container, ExchangeRateTable, CurrencyTable

load_dotenv()

app = FastAPI()


@app.on_event('startup')
@inject
def on_startup():
    container = Container()
    container.config.database.database_url.from_env('DATABASE_URL')
    container.wire(modules=[sys.modules[__name__]])


@app.get('/conversion_rate/{base}/{target}')
@inject
def current_conversion_rate(base: str, target: str,
                            exchange_rate_table: ExchangeRateTable = Depends(Provide[Container.exchange_rate_table]),
                            currency_table: CurrencyTable = Depends(Provide[Container.currency_table])):
    rate = exchange_rate_table.get_exchange_rate(base, target)
    if rate:
        return rate
    print('Not found currency in db')
    url = f'https://v6.exchangerate-api.com/v6/{os.getenv("EXCHANGE_API_KEY")}/pair/{base}/{target}'
    response = requests.get(url)
    data = response.json()
    conversion_rate = data['conversion_rate']
    currency_table.save_currency(base)
    currency_table.save_currency(target)
    base_id = currency_table.get_currency_id(base)
    target_id = currency_table.get_currency_id(target)
    exchange_rate_table.save_exchange_rate(base_id, target_id, conversion_rate)
    return conversion_rate


@app.get('/conversion/{base}/{target}/{amount}')
@inject
def currency_conversion_handler(base: str, target: str, amount: int,
                                exchange_rate_table: ExchangeRateTable = Depends(
                                    Provide[Container.exchange_rate_table]),
                                currency_table: CurrencyTable = Depends(Provide[Container.currency_table])):
    conversion = exchange_rate_table.currency_conversion(base, target, amount)
    if conversion:
        return conversion
    print('Not found currency in db')
    url = f'https://v6.exchangerate-api.com/v6/{os.getenv("EXCHANGE_API_KEY")}/pair/{base}/{target}'
    response = requests.get(url)
    data = response.json()
    conversion_rate = data['conversion_rate']
    currency_table.save_currency(base)
    currency_table.save_currency(target)
    base_id = currency_table.get_currency_id(base)
    target_id = currency_table.get_currency_id(target)
    exchange_rate_table.save_exchange_rate(base_id, target_id, conversion_rate)
    conversion = exchange_rate_table.currency_conversion(base, target, amount)
    return conversion
