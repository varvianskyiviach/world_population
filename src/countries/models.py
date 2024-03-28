from pydantic import BaseModel


class CountryInfo(BaseModel):
    country_name: str
    population: int
    region: str

    def __str__(self) -> str:
        return f"Country {self.country_name}, population: {self.population}, {self.region}"
