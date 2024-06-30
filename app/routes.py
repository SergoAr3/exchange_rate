from dotenv import load_dotenv
from fastapi import APIRouter

from app.db.queries import exchange_rate_table
from app.services import exchangerate_api_request

load_dotenv()

router = APIRouter()



@router.get('/conversion_rate/{base}/{target}')
async def current_conversion_rate(base: str, target: str):
    rate = await exchange_rate_table.get_exchange_rate(base, target)
    if rate:
        return rate
    conversion_rate = await exchangerate_api_request(base, target)
    return conversion_rate


@router.get('/conversion/{base}/{target}/{amount}')
async def currency_conversion_handler(base: str, target: str, amount: int):
    conversion = await exchange_rate_table.currency_conversion(base, target, amount)
    if conversion:
        return conversion
    conversion = await exchangerate_api_request(base, target, amount=amount, conversion=True)
    return conversion
