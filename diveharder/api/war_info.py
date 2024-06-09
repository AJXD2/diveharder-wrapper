from diveharder.api.base import ApiBase
from diveharder.objects import WarInfo


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
