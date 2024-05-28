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
