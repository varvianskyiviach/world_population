from typing import List

from countries.models import CountryInfo
from database.session import Session

from .constant import QUERY_FETCH, QUERY_LOAD


class CountriesCRUD(Session):
    def __init__(self, dsn: str) -> None:
        super().__init__(dsn)

    async def save(self, countries: List[CountryInfo]) -> None:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                for country in countries:
                    await connection.execute(
                        QUERY_LOAD,
                        country.country_name,
                        country.population,
                        country.region,
                    )

    async def get(self) -> dict:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                results = await connection.fetch(QUERY_FETCH)
            for row in results:
                processing_row = dict(row)
                print(processing_row)
