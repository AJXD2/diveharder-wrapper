from functools import lru_cache
from typing import Generator, List, Optional

from requests import Response
from diveharder.api.base import ApiBase
from diveharder.objects import Dispatch, MajorOrder


class Dispatches(ApiBase):
    """
    Class for interacting with the Dive Harder API's news feed.
    """

    @lru_cache(maxsize=1)
    def get_dispatches(self) -> Generator[Dispatch, None, None]:
        """
        Get a list of all dispatches from the news feed.

        Yields:
            Dispatch: The next dispatch from the news feed.
        """

        for i in self._api_request("news_feed"):
            yield Dispatch.from_json(self._client, i)

    def get_dispatch(self, id: int) -> Optional[Dispatch]:
        """
        Get a specific dispatch from the news feed by ID.

        Args:
            id (int): ID of the dispatch to retrieve.

        Returns:
            Optional[Dispatch]: Dispatch object if found, None otherwise.
        """

        dispatches = self.get_dispatches()
        for dispatch in dispatches:
            if dispatch["id"] == id:
                return dispatch

        return None

    def get_latest_dispatch(self) -> Dispatch:
        """
        Get the most recent dispatch from the news feed.

        Returns:
            Dispatch: The most recent dispatch.
        """

        dispatches = self.get_dispatches()
        return list(dispatches)[-1]

    def get_latest_dispatches(self, count: int) -> List[Dispatch]:
        """
        Get the most recent dispatches from the news feed.

        Args:
            count (int): The number of dispatches to retrieve.

        Returns:
            List[Dispatch]: The most recent dispatches.
        """

        dispatches = list(self.get_dispatches())
        return dispatches[-count:]

    def get_major_order(self) -> MajorOrder:
        """
        Retrieves the major order from the API and returns it as a `MajorOrder` object.

        Returns:
            MajorOrder: The major order retrieved from the API.
        """
        major_order = self._api_request("major_order")
        if isinstance(major_order, Response):
            return None
        return MajorOrder.from_json(self._client, major_order)
