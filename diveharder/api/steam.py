from diveharder.api.base import BaseApiModule
import typing
import diveharder.models as models

if typing.TYPE_CHECKING:
    from diveharder.api_client import ApiClient


class SteamModule(BaseApiModule):
    """
    The Steam API module.
    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_all_steam_news(self) -> typing.List[models.SteamNews]:
        """
        Gets the information about the current war.
        """
        data = self.get("community", "api", "v1", "steam")

        return [models.SteamNews(**news) for news in data]

    def get_steam_news(self, gid: str) -> models.SteamNews:
        """
        Gets the information about the current war.
        """
        data = self.get("community", "api", "v1", "steam", gid)
        return models.SteamNews(**data)
