import typing
import requests

if typing.TYPE_CHECKING:
    from diveharder.api_client import ApiClient


class BaseApiModule:
    """
    The base class for all API modules.
    """

    def __init__(self, api_client: "ApiClient") -> None:
        self.api_client = api_client
        self.logger = api_client.logger
        self.session = api_client.session
        self.diveharder_url = api_client.api_config.diveharder
        self.community_url = api_client.api_config.community

    def get(self, url: typing.Literal["diveharder", "community"], *path) -> typing.Dict:
        """
        Sends a GET request to the specified URL.
        """
        try:
            response = self.session.get(
                url=f"{self.diveharder_url if url == 'diveharder' else self.community_url}/{'/'.join(path)}",
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTPError: {e}")
            return {}
