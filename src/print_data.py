import asyncio
import os
from typing import List

from config.settings import DSN
from countries.models import RegionInfo
from countries.repository import CountriesCRUD


async def main() -> None:
    db_manager = CountriesCRUD(DSN)

    await db_manager.connect()
    regions: List[RegionInfo] = await db_manager.list()
    await db_manager.close()

    if regions is not None:
        for region in regions:
            print(region.repr())

        print(f"<<<Source of data is - 👉[{os.getenv('SOURCE', default='')}]👈>>>")


asyncio.run(main())
