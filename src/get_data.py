import asyncio
import os
from typing import List

from config.settings import DSN
from countries.models import CountryInfo
from countries.parsers import ParserWiki
from countries.repository import CountriesCRUD

PARSERS_MAPPING = {
    "wikipedia": ParserWiki(),
}


async def get_data():
    try:
        source = os.getenv("SOURCE", default="")
        parser = PARSERS_MAPPING[source]
        result = List[CountryInfo] = await parser.get_all_data()
    except Exception:
        print(f"Parser '{source}' has not been found! Make sure you have created parser and added in PARSERS_MAPPING")

    return result


result = asyncio.run(get_data())


async def save_in_db(countries):

    db_manager = CountriesCRUD(dsn=DSN)

    await db_manager.connect()
    await db_manager.save(countries)
    await db_manager.close()


asyncio.run(save_in_db(countries=result))
