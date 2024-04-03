from typing import List

from asyncpg.exceptions import UndefinedTableError, UniqueViolationError

from countries.constant import QUERY_FETCH, QUERY_LOAD
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
                        result = await connection.execute(
                            QUERY_LOAD,
                            country.country_name,
                            country.population,
                            country.region,
                            country.data_source,
                            country.country_name,
                            country.data_source,
                        )
                        if result == "INSERT 0 0":
                            print(
                                f"""❌ Country '{country.country_name}' from source '{country.data_source}' already exists in the database!\n"""  # noqa
                            )
                        else:
                            print(
                                f"""✅ Country '{country.country_name}' from source '{country.data_source}' has been saved in database\n"""  # noqa
                            )
                    except UniqueViolationError as e:
                        print(f"{e}")

    async def list(self, data_source: str) -> List[RegionInfo]:
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                try:
                    results = await connection.fetch(QUERY_FETCH, data_source)
                    regions: List[RegionInfo] = []
                    for result in results:
                        data = dict(result)
                        regions.append(RegionInfo(**data))

                    return regions

                except UndefinedTableError:
                    print(
                        """❗ Table 'countries' does not exist. First make sure that the container with postgresql is running and database is initialised!"""  # noqa
                    )

        return []
