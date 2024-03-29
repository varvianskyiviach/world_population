import asyncio
import os
from typing import List

from config.settings import DSN, PARSERS_MAPPING
from countries.models import CountryInfo
from countries.parsers import GeonamesAPI, ParserWiki  # noqa: F401, F403
from countries.repository import CountriesCRUD
from database.service import Service


async def get_data(parser) -> List[CountryInfo]:
    result: List[CountryInfo] = await parser.get_all_data()

    return result


async def save_in_db(countries):
    service = Service(dsn=DSN)
    await service.connect()
    await service.create_table()
    await service.close()

    db_manager = CountriesCRUD(dsn=DSN)
    await db_manager.connect()
    await db_manager.save(countries)
    await db_manager.close()


async def main():
    source = os.getenv("SOURCE", default="")
    parser_name = PARSERS_MAPPING.get(source)
    try:
        parser_class = globals()[parser_name]
        parser = parser_class()
        result = await get_data(parser)
    except KeyError:
        print(f"Parser '{source}' has not been found! Make sure you have created parser and added in PARSERS_MAPPING")
        return None

    await save_in_db(countries=result)


asyncio.run(main())
