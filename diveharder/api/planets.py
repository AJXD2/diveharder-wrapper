from diveharder.api.base import BaseApiModule
import typing
import diveharder.models as models

if typing.TYPE_CHECKING:
    from diveharder.api_client import ApiClient


class PlanetsModule(BaseApiModule):
    """
    The Planets API module.
    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_planets(self) -> typing.List[models.Planet]:
        """Get all planets

        Returns:
            typing.List[models.Planet]: The list of planet objects
        """
        data = self.get("community", "api", "v1", "planets")
        return [models.Planet(**planet) for planet in data]

    def get_planet(self, index: int) -> models.Planet:
        """Gets a planet using the index

        Args:
            index (int): The index of the planet

        Returns:
            models.Planet: The planet object
        """
        data = self.get("community", "api", "v1", "planets", str(index))
        return models.Planet(**data)

    def get_all_planets_with_events(self) -> typing.List[models.Planet]:
        """Gets all planets with an active event

        Returns:
            typing.List[models.Planet]: The list of planet objects
        """
        data = self.get("community", "api", "v1", "planet-events")
        return [models.Planet(**planet) for planet in data]
