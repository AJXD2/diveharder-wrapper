from functools import lru_cache
from typing import Generator, Optional
from diveharder.api.base import ApiBase
from diveharder.objects import Biome, Enviromental, Planet


class Planets(ApiBase):
    """
    Provides methods for retrieving information about planets from the API.
    """

    @lru_cache(maxsize=1)
    def get_planets(self) -> Generator[Planet, None, None]:
        """
        Retrieves information about all planets from the API.

        Yields:
            Planet: Information about each planet.
        """
        data = self._api_request("planets")
        for index, planet_data in data.items():
            planet_data["id"] = index
            yield Planet.from_json(self._client, planet_data)

    def get_planet(self, id: int) -> Optional[Planet]:
        """
        Retrieves information about a specific planet from the API.

        Args:
            id (int): The ID of the planet.

        Returns:
            Optional[Planet]: Information about the planet if found, None otherwise.
        """
        for i in self.get_planets():
            if int(i.id) == int(id):
                return i

        return None

    def get_planets_by_enviromental(
        self, enviromental: Enviromental
    ) -> Generator[Planet, None, None]:
        """
        Retrieves information about planets that have a specific environmental.

        Args:
            enviromental (Enviromental): The environmental to filter by.

        Yields:
            Planet: Information about each planet with the specified environmental.
        """
        for i in self.get_planets():
            for j in i.enviromentals:
                if enviromental == j:
                    yield i

    def get_planets_by_biome(self, biome: Biome) -> Generator[Planet, None, None]:
        """
        Retrieves information about planets that have a specific biome.

        Args:
            biome (Biome): The biome to filter by.

        Yields:
            Planet: Information about each planet with the specified biome.
        """
        for i in self.get_planets():
            if biome == i.biome:
                yield i

    def __getitem__(self, item):
        """
        Retrieves information about a specific planet from the API using the planet's ID.

        Args:
            item (int): The ID of the planet.

        Returns:
            Optional[Planet]: Information about the planet if found, None otherwise.
        """
        return self.get_planet(item)
