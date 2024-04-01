from typing import List

from asyncpg.exceptions import UndefinedTableError, UniqueViolationError

from countries.constant import QUERY_FETCH, QUERY_LOAD, TABLE_NAME
from countries.models import CountryInfo, RegionInfo
from database.session import Session


class CountriesCRUD(Session):
    def __init__(self, dsn: str) -> None:
        super().__init__(dsn)

    async def save(self, countries: List[CountryInfo]) -> None:
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                for country in countries:
                    try:
                        await connection.execute(
                            QUERY_LOAD,
                            country.country_name,
                            country.population,
                            country.region,
                        )
                        print(f"{country.country_name} has been saved in database\n")
                    except UniqueViolationError as e:
                        print(f"{e}")

    async def list(self) -> List[RegionInfo]:
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                try:
                    results = await connection.fetch(QUERY_FETCH)
                    regions: List[RegionInfo] = []
                    for result in results:
                        data = dict(result)
                        regions.append(RegionInfo(**data))

                    return regions

                except UndefinedTableError:
                    print(f"Table '{TABLE_NAME}' does not exist. First you should get data, run get_data conteiner!")

        return []
