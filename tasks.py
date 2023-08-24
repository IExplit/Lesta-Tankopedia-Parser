from ttc import get_ttc
import asyncio
import aiohttp

URL = 'https://tanki.su/ru/tankopedia/'

HEADERS = {
    'authority': 'tanki.su',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.2.767 Yowser/2.5 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


async def get_tasks(
        nation='', # Фильтр по нации танка
        tankType='', # Фильтр по типу танка
        role='', # Фильтр по роли танка
        tier='', # Фильтр по уровню танка
        premium='', # Фильтр по премиаьлности танка
        collector_vehicle='' # Фильтр по коллекционности танка
):
    data = {
        'filter[nation]': nation,
        'filter[type]': tankType,
        'filter[role]': role,
        'filter[tier]': tier,
        'filter[language]': 'ru',
        'filter[premium]': premium,
        'filter[collector_vehicle]': collector_vehicle
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://tanki.su/wotpbe/tankopedia/api/vehicles/by_filters/',
                headers=HEADERS,
                data=data,
        ) as response:
            response = await response.json()
            tasks = [asyncio.create_task(get_ttc(session,ttc[3], ttc[0], ttc[4], ttc[7])) for ttc in response['data']['data']]
            await asyncio.gather(*tasks)