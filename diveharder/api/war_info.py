from diveharder.api.base import ApiBase
from diveharder.objects import Planet, PlanetInfo, WarInfo


class WarInfoAPI(ApiBase):
    """
    Class used to interact with the War Info API endpoint.
    """

    def get_war_info(self) -> WarInfo:
        """
        Get infromation about the current war.

        Returns:
            WarInfo: Information about the current war.
        """

        return WarInfo.from_json(self._client, self._api_request("war_info"))

    def get_planet_info(self, planet: Planet) -> PlanetInfo:
        for i in self.get_war_info().planet_infos:
            if i._index == planet.id:
                return i

        return None
