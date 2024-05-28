from diveharder.api.base import ApiBase
from diveharder.objects import GalaxyStatistics, GlobalStatistics, PlanetStatistics


class Statistics(ApiBase):
    def get_global_statistics(self) -> GlobalStatistics:
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
        statistics = self._api_request("planet_stats").get("planets_stats")

        for i in statistics:
            if i["planetIndex"] == planet_id:
                return PlanetStatistics.from_json(self.client, i)

        return None

    def get_galaxy_statistics(self) -> GalaxyStatistics:
        statistics = self._api_request("planet_stats")

        return GalaxyStatistics.from_json(self.client, statistics["galaxy_stats"])
