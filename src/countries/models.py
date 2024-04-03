from pydantic import BaseModel


class CountryInfo(BaseModel):
    country_name: str
    population: int
    region: str
    data_source: str

    def __str__(self) -> str:
        return f"Country {self.country_name}, population: {self.population}, {self.region}, {self.data_source}"


class RegionInfo(BaseModel):
    region: str
    total_population: int
    largest_country: str
    max_population_country: int
    smallest_country: str
    min_population_country: int

    def repr(self) -> str:
        return "\n".join(
            (
                f"========================= The Region 👉 {self.region} ============================",
                f"Total population in region 👉 {self.total_population:,}",
                f"The largest country in region 👉 {self.largest_country}",
                f"Max population country in region 👉 {self.max_population_country:,}",
                f"The smallest country in region 👉 {self.smallest_country}",
                f"Min population country in region 👉 {self.min_population_country:,}",
                f"\n",  # noqa
            )
        )
