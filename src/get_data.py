import asyncio
from typing import List

from config.settings import DSN, PARSERS_MAPPING, SOURCE
from countries.models import CountryInfo
from countries.parsers import (  # noqa: F401, F403
    GeonamesAPI,
    ParserWiki,
    StatisticsTimes,
)
from countries.repository import CountriesCRUD


async def get_data(parser) -> List[CountryInfo]:
    result: List[CountryInfo] = await parser.get_all_data()

    return result


async def save_in_db(countries):
    db_manager = CountriesCRUD(dsn=DSN)

    await db_manager.connect()
    await db_manager.save(countries)
    await db_manager.close()


async def main():
    data_source = SOURCE
    parser_name = PARSERS_MAPPING.get(data_source)[0]
    url_source = PARSERS_MAPPING.get(data_source)[1]
    try:
        parser_class = globals()[parser_name]
        parser = parser_class(url_source, data_source)
        result = await get_data(parser)
    except KeyError:
        print(
            f"Parser '{data_source}' has not been found! Make sure you have created parser and added in PARSERS_MAPPING"
        )
        return None

    await save_in_db(countries=result)


asyncio.run(main())
