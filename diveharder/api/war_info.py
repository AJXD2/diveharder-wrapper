from diveharder.api.base import ApiBase
from diveharder.objects import WarInfo


class WarInfoAPI(ApiBase):

    def get_war_info(self) -> WarInfo:
        """
        Get infromation about the current war.

        Returns:
            WarInfo: Information about the current war.
        """
        # the v1 endpoint is returning a 500 error code at this time.
        # TODO: If it is fixed, the `raw=True` should be removed.
        return WarInfo.from_json(self._client, self._api_request("war_info", raw=True))
