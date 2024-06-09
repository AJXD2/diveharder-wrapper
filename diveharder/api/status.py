from functools import lru_cache
from typing import Generator, List
from diveharder.api.base import ApiBase
from diveharder.objects import Planet, PlanetStatus, Status


class StatusAPI(ApiBase):
    """
    Class for interacting with the Helldivers 2 Status API.
    """

    @lru_cache(maxsize=1)
    def get_status(self) -> Status:
        """
        Retrieves the status of the API from the API.

        Returns:
            Status: The status retrieved from the API.
        """
        return Status.from_json(self.client, self._api_request("status"))

    def get_planet_status(self, planet: Planet) -> PlanetStatus:
        """
        Retrieves the status of a planet from the API.

        Args:
            planet (Planet): The planet to retrieve status for.

        Returns:
            PlanetStatus: The status retrieved from the API.
        """
        for status in self.get_status().planet_status:
            if status._planet == planet.id:
                return status

        return None

    def get_planets_status(self) -> Generator[PlanetStatus, None, None]:
        """
        Retrieves the status of all planets from the API.

        Yields:
            PlanetStatus: The status of each planet.
        """
        for status in self.get_status().planet_status:
            yield PlanetStatus.from_json(self.client, status)
