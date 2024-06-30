from loguru import logger

import os
from dotenv import load_dotenv
import requests
from app.db.queries import currency_table, exchange_rate_table

load_dotenv()


async def exchangerate_api_request(base, target, conversion: bool = False, amount: float = None):
    logger.info('Not found currency in db')
    url = f'https://v6.exchangerate-api.com/v6/{os.getenv("EXCHANGE_API_KEY")}/pair/{base}/{target}'
    response = requests.get(url)
    data = response.json()
    conversion_rate = data['conversion_rate']
    await currency_table.save_currency(base)
    await currency_table.save_currency(target)
    base_id = await currency_table.get_currency_id(base)
    target_id = await currency_table.get_currency_id(target)
    await exchange_rate_table.save_exchange_rate(base_id, target_id, conversion_rate)
    if conversion:
        conversion = await exchange_rate_table.currency_conversion(base, target, amount)
        return conversion
    return conversion_rate
