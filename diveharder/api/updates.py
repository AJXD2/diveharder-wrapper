from datetime import datetime
from typing import Generator, Optional
from diveharder.api.base import ApiBase
from diveharder.objects import Update


class UpdatesAPI(ApiBase):
    """API class for retrieving updates from the DiveHarder API."""

    def get_updates(self) -> Generator[Update, None, None]:
        """
        Retrieves updates from the DiveHarder API and returns them as a generator of Update objects.

        Returns:
            Generator[Update]: A generator that yields Update objects.
        """
        updates = self._api_request("updates")

        for i in updates:
            yield Update.from_json(self, i)

    def get_update_by_date(self, date: str) -> Optional[Update]:
        """
        Get an update by its date.

        Args:
            date (str): The date of the update in the format "%d-%b-%Y %H:%M".

        Returns:
            Update or None: The update object with the given date, or None if no update is found.
        """
        date = datetime.strptime(date, "%d-%b-%Y %H:%M")

        for i in self.get_updates():
            if i.date == date:
                return i
        return None

    def get_update_by_url(self, url: str) -> Optional[Update]:
        """
        Get an update by its URL.

        Args:
            url (str): The URL of the update.

        Returns:
            Update or None: The update object with the given URL, or None if no update is found.
        """
        for i in self.get_updates():
            if i.url == url:
                return i
        return None

    def get_update_by_title(self, title: str) -> Optional[Update]:
        """
        Get an update by its title.

        Args:
            title (str): The title of the update.

        Returns:
            Update or None: The update object with the given title, or None if no update is found.
        """
        for i in self.get_updates():
            if i.title == title:
                return i
        return None

    def get_latest_update(self) -> Update:
        """
        Get the latest update.

        Returns:
            Update: The latest update.
        """
        return list(self.get_updates())[-1]
