import json
from abc import ABC, abstractmethod
from difflib import SequenceMatcher
from pathlib import Path
from typing import List

import aiofiles
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from config.settings import FILE_JSON_PATH, HEADERS, PARAMS
from countries.models import CountryInfo


class ParserInterface(ABC):

    @abstractmethod
    def __init__(self, url_source, data_source) -> None:
        pass

    @abstractmethod
    async def _extract_data(self) -> List[dict]:
        pass

    @abstractmethod
    async def get_all_data(self) -> List[CountryInfo]:
        pass


class ParserWiki(ParserInterface):
    filepath = FILE_JSON_PATH
    headers = HEADERS

    def __init__(self, url_source, data_source) -> None:
        self.url_source = url_source
        self.data_source = data_source

    def similar(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    async def _extract_data(self) -> List[dict]:
        async with ClientSession() as session:
            async with session.get(url=self.url_source, headers=self.headers) as responce:
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
                    web_data: list[dict] = []
                    for row in results_table[2:]:
                        columns = row.find_all("td")
                        try:
                            country_name = columns[1].select("td > a")[0].get_text()
                            population = int((columns[2].text).replace(",", ""))
                        except (IndexError, AttributeError):
                            country_name = columns[0].select("td > a")[0].get_text()
                            population = int((columns[1].text).replace(",", ""))

                        web_data.append({"country_name": country_name, "population": population})
                else:
                    print("Results has not found")

                return web_data

    async def _extract_data_additional(self, filepath: Path, web_data: List[dict]) -> List[dict]:

        async with aiofiles.open(f"{filepath}", mode="r") as file:
            contents = await file.read()
            file_data: List[dict] = json.loads(contents).get("geonames")

            additional_data: list[dict] = []
            for base_country in web_data:
                best_match_ratio = 0.0
                best_match_country = None
                for country in file_data:
                    ratio: float = self.similar(base_country["country_name"], country["countryName"])
                    if ratio >= 0.3 and ratio >= best_match_ratio:
                        best_match_ratio = ratio
                        best_match_country = country
                        region = best_match_country["continentName"]

                if region:
                    additional_data.append({"country_name": base_country["country_name"], "region": region})

            return additional_data

    async def get_all_data(self) -> List[CountryInfo]:

        web_data: List[dict] = await self._extract_data()
        additional_data: List[dict] = await self._extract_data_additional(
            filepath=self.filepath,
            web_data=web_data,
        )

        results: List[CountryInfo] = []

        for main_data in web_data:
            main_data["data_source"] = self.data_source
            for data in additional_data:
                if main_data["country_name"] == data["country_name"]:
                    main_data["region"] = data["region"]
                    if main_data["population"] > 0:
                        results.append(CountryInfo(**main_data))

        return results


class GeonamesAPI(ParserInterface):
    params = PARAMS

    def __init__(self, url_source, data_source) -> None:
        self.url_source = url_source
        self.data_source = data_source

    async def _extract_data(self) -> List[dict]:
        async with ClientSession() as session:
            async with session.get(self.url_source, params=self.params) as responce:

                row_data: dict = await responce.json()
                countries_info: List[dict] = row_data.get("geonames", [])

                web_data: list[dict] = []
                for country in countries_info:

                    web_data.append(
                        {
                            "country_name": country["countryName"],
                            "population": int(country["population"]),
                            "region": country["continentName"],
                        },
                    )

            return web_data

    async def get_all_data(self) -> List[CountryInfo]:
        web_data: List[dict] = await self._extract_data()

        results: List[CountryInfo] = []
        for data in web_data:
            data["data_source"] = self.data_source
            if data["population"] > 0:
                results.append(CountryInfo(**data))

        return results


class StatisticsTimes(ParserInterface):
    headers = HEADERS

    def __init__(self, url_source, data_source) -> None:
        self.url_source = url_source
        self.data_source = data_source

    async def _extract_data(self) -> List[dict]:
        async with ClientSession() as session:
            async with session.get(self.url_source, headers=self.headers) as responce:
                html_content = await responce.text()
                soup = BeautifulSoup(html_content, "html.parser")

                table = soup.find("table", id="table_id")
                if table is not None:
                    tbody = table.find("tbody")
                else:
                    print("Table has not found")
                if tbody is not None:
                    results_table: List = tbody.find_all("tr")
                else:
                    print("Body`s table has not found")

                web_data: list[dict] = []
                for row in results_table:
                    colums = row.find_all("td")
                    try:
                        country_name: str = colums[0].get_text()
                        population: int = int(colums[3].get_text().replace(",", ""))
                        region: str = colums[9].get_text()
                    except Exception as e:
                        print(f"Error {e}")

                    web_data.append(
                        {
                            "country_name": country_name,
                            "population": population,
                            "region": region,
                        },
                    )

                return web_data

    async def get_all_data(self) -> List[CountryInfo]:
        web_data: List[dict] = await self._extract_data()

        results: List[CountryInfo] = []

        for data in web_data:
            data["data_source"] = self.data_source
            if data["population"] > 0:
                results.append(CountryInfo(**data))

        return results
