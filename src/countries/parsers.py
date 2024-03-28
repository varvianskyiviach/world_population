import json
from abc import ABC, abstractmethod
from difflib import SequenceMatcher
from typing import List

import aiofiles
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from config.settings import FILE_JSON_PATH, HEADERS
from countries.models import CountryInfo


class ParserInterface(ABC):
    @abstractmethod
    async def extract_data(self) -> List[dict]:
        pass

    @abstractmethod
    def get_all_data(self) -> List[CountryInfo]:
        pass


class ParserWiki(ParserInterface):
    URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    FILEPATH = FILE_JSON_PATH

    @staticmethod
    def similar(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    async def extract_data(self) -> List[dict]:
        async with ClientSession() as session:
            async with session.get(url=self.URL, headers=HEADERS) as responce:
                html_content = await responce.text()
                soup = BeautifulSoup(html_content, "html.parser")

                table = soup.find(
                    "table",
                    class_="wikitable sortable sticky-header sort-under mw-datatable col2left col6left",
                )
                if table is not None:
                    tbody = table.find("tbody")
                    if tbody is not None:
                        results_table = tbody.find_all("tr")
                    else:
                        print("Body`s table has not found")
                else:
                    print("Table has not found")

                if results_table:
                    data: list[dict] = []
                    for row in results_table[2:]:
                        columns = row.find_all("td")
                        try:
                            country_name = columns[1].select("td > a")[0].get_text()
                            population = int((columns[2].text).replace(",", ""))
                        except (IndexError, AttributeError) as e:
                            country_name = columns[0].select("td > a")[0].get_text()
                            population = int((columns[1].text).replace(",", ""))
                            print(f"Error: {e}")

                        data.append({"country_name": country_name, "population": population})
                else:
                    print("Results has not found")

                return data

    async def extract_data_additional(self, filepath: str, web_data: List[dict]) -> List[dict]:

        async with aiofiles.open(f"{filepath}", mode="r") as file:
            contents = await file.read()
            file_data: dict = json.loads(contents)
            file_data: list[dict] = file_data.get("geonames")

            additional_data: list[dict] = []
            for base_country in web_data:
                best_match_ratio = 0.0
                best_match_country = None
                for country in file_data:
                    ratio: float = ParserWiki.similar(base_country["country_name"], country["countryName"])
                    if ratio >= 0.3 and ratio >= best_match_ratio:
                        best_match_ratio = ratio
                        best_match_country = country
                        region = best_match_country["continentName"]

                if region:
                    additional_data.append({"country_name": base_country["country_name"], "region": region})

            return additional_data

    async def get_all_data(self) -> List[CountryInfo]:

        web_data: List[dict] = await self.extract_data()
        additional_data: List[dict] = await self.extract_data_additional(
            filepath=self.FILEPATH,
            web_data=web_data,
        )

        results: List[CountryInfo] = []

        for main_data in web_data:
            for data in additional_data:
                if main_data["country_name"] == data["country_name"]:
                    main_data["region"] = data["region"]

                    results.append(CountryInfo(**main_data))

        return results
