from typing import List

from asyncpg.exceptions import UniqueViolationError

from countries.constant import QUERY_FETCH, QUERY_LOAD
from countries.models import CountryInfo, RegionInfo
from database.session import Session


class CountriesCRUD(Session):
    def __init__(self, dsn: str) -> None:
        super().__init__(dsn)

    async def save(self, countries: List[CountryInfo]) -> None:
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

    async def list(self):
        async with self.pool.acquire() as connection:

            results = await connection.fetch(QUERY_FETCH)
            regions: List[RegionInfo] = []
            for result in results:
                data = dict(result)
                regions.append(RegionInfo(**data))

            for region in regions:
                print(region.repr())
