from functools import lru_cache
from typing import Generator, List, Optional
from diveharder.api.base import ApiBase
from diveharder.objects import Campaign, Planet


class Campaigns(ApiBase):
    @lru_cache(maxsize=1)
    def get_campaigns(self) -> Generator[Campaign, None, None]:
        data = self._api_request("status").get("campaigns")
        for i in data:
            yield Campaign.from_json(self._client, i)

    def get_campaign_by_planet(self, planet: Planet) -> Optional[Campaign]:

        for i in self.get_campaigns():
            if i.planet.id == planet.id:
                return i

        return None
