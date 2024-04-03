import asyncio
from typing import List

from config.settings import DSN, SOURCE
from countries.models import RegionInfo
from countries.repository import CountriesCRUD


async def main() -> None:
    db_manager = CountriesCRUD(dsn=DSN)

    await db_manager.connect()
    regions: List[RegionInfo] = await db_manager.list(data_source=SOURCE)
    await db_manager.close()

    if regions is not None and len(regions) > 0:
        for region in regions:
            print(region.repr())

        print(f"<<<Source of data is - 👉[{SOURCE}]👈>>>")

    else:
        print(
            f"""❗Data from '{SOURCE}' has not been find. First you should get data, run 'get_data' conteiner! - <docker compose up get_data>"""  # noqa
        )


asyncio.run(main())
