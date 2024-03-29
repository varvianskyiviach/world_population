import asyncio

from config.settings import DSN
from countries.repository import CountriesCRUD


async def main():
    db_manager = CountriesCRUD(DSN)

    await db_manager.connect()
    await db_manager.list()
    await db_manager.close()


asyncio.run(main())
