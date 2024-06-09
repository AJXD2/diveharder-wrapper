from diveharder.api.base import ApiBase
from diveharder.objects import GalaxyStatistics, GlobalStatistics, PlanetStatistics


class Statistics(ApiBase):
    """
    Class used to interact with the Statistics API endpoint.
    """

    def get_global_statistics(self) -> GlobalStatistics:
        """
        Retrieves global statistics from the API.

        Returns:
            GlobalStatistics: The global statistics.
        """
        statistics = self._api_request("planet_stats")

        return GlobalStatistics(
            self,
            GalaxyStatistics.from_json(self.client, statistics["galaxy_stats"]),
            [
                PlanetStatistics.from_json(
                    self.client,
                    i,
                )
                for i in statistics["planets_stats"]
            ],
        )

    def get_planet_statistics(self, planet_id: int) -> PlanetStatistics:
        """
        Retrieves statistics for a specific planet from the API.

        Args:
            planet_id (int): The ID of the planet.

        Returns:
            PlanetStatistics: The statistics of the planet.
        """
        statistics = self._api_request("planet_stats").get("planets_stats")

        for i in statistics:
            if i["planetIndex"] == planet_id:
                return PlanetStatistics.from_json(self.client, i)

        return None

    def get_galaxy_statistics(self) -> GalaxyStatistics:
        """
        Retrieves statistics for the galaxy from the API.

        Returns:
            GalaxyStatistics: The statistics of the galaxy.
        """
        statistics = self._api_request("planet_stats")

        return GalaxyStatistics.from_json(self.client, statistics["galaxy_stats"])
