from functools import lru_cache
from diveharder.api.base import ApiBase
from diveharder.objects import Planet, PlanetStatus, Status


class StatusAPI(ApiBase):

    @lru_cache(maxsize=1)
    def get_status(self) -> Status:
        """
        Retrieves the status of the API from the API and returns it as a `dict` object.

        Returns:
            dict: The status retrieved from the API.
        """
        return Status.from_json(self.client, self._api_request("status"))

    def get_planet_status(self, planet: Planet) -> PlanetStatus:
        """
        Retrieves the status of a planet from the API and returns it as a `dict` object.

        Returns:
            dict: The status retrieved from the API.
        """
        for i in self.get_status()["planetStatus"]:
            if i["index"] == planet.id:
                return PlanetStatus.from_json(self.client, planet, i)

        return None
