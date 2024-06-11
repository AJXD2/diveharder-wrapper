from functools import lru_cache
from typing import Generator, Optional
from diveharder.api.base import ApiBase
from diveharder.objects import Campaign, Planet


class Campaigns(ApiBase):
    """
    Provides methods to interact with the Campaigns API endpoint.
    """

    @lru_cache(maxsize=1)
    def get_campaigns(self) -> Generator[Campaign, None, None]:
        """
        Retrieves campaign data from the API and returns it as a generator of Campaign objects.

        Returns:
            Generator[Campaign]: A generator that yields Campaign objects.
        """
        data = self._api_request("status").get("campaigns")
        for i in data:
            yield Campaign.from_json(self._client, i)

    def get_campaign_by_planet(self, planet: Planet) -> Optional[Campaign]:
        """
        Retrieves the campaign that corresponds to the given planet.

        Args:
            planet (Planet): The planet to search for.

        Returns:
            Optional[Campaign]: The corresponding Campaign object, or None if not found.
        """
        for i in self.get_campaigns():
            if i.planet.id == planet.id:
                return i

        return None
