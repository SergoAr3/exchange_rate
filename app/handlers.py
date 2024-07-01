from dotenv import load_dotenv
from fastapi import APIRouter, Depends

from app.db.queries import ExchangeRateTable
from app.services import ExchangeRate

load_dotenv()

router = APIRouter()


@router.get('/conversion_rate/{base}/{target}')
async def current_conversion_rate(
        base: str,
        target: str,
        controller_postgres: ExchangeRateTable = Depends(),
        controller_exchange: ExchangeRate = Depends()
):
    rate = await controller_postgres.get_exchange_rate(base, target)
    if rate:
        return rate
    conversion_rate = await controller_exchange.exchangerate_api_request(base, target)
    return conversion_rate


@router.get('/conversion/{base}/{target}/{amount}')
async def currency_conversion_handler(
        base: str,
        target: str,
        amount: int,
        controller_postgres: ExchangeRateTable = Depends(),
        controller_exchange: ExchangeRate = Depends()
):
    conversion = await controller_postgres.currency_conversion(base, target, amount)
    if conversion:
        return conversion
    conversion = await controller_exchange.exchangerate_api_request(base, target, amount=amount, conversion=True)
    return conversion
