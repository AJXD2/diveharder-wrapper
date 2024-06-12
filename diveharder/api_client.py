from datetime import datetime
import logging
from time import time
import requests
from requests.adapters import HTTPAdapter, Retry

from diveharder.api.campaings import Campaigns
from diveharder.api.dispatches import Dispatches
from diveharder.api.planets import Planets
from diveharder.api.stats import Statistics
from diveharder.api.status import StatusAPI
from diveharder.api.updates import UpdatesAPI
from diveharder.api.war_info import WarInfoAPI
from diveharder.constants import OFFICIAL_DIVEHARDER_URL


def retry_adapter(
    backoff_factor: float, retries: int, extra_retry_codes: list
) -> HTTPAdapter:
    """Configures an HTTP adapter with retries and backoff."""
    retry_codes = [429] + extra_retry_codes
    retry_strategy = Retry(
        total=retries,
        status_forcelist=retry_codes,
        backoff_factor=backoff_factor,
        allowed_methods=["GET"],
    )
    return HTTPAdapter(max_retries=retry_strategy)


def set_logger(debug: bool) -> None:
    """Configures debug logging if requested."""
    level = logging.DEBUG if debug else logging.ERROR
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.propagate = True


class DiveHarderApiClient:
    def __init__(
        self,
        user_agent: str = f"DiveHarderAPIWrapper",
        url: str = OFFICIAL_DIVEHARDER_URL,
        retry_count: int = 5,
        backoff_factor: float = 0.2,
        debug: bool = False,
    ) -> None:
        self._url = url
        self._session = requests.Session()
        self._session.mount("https://", retry_adapter(backoff_factor, retry_count, []))
        self._user_agent = user_agent
        set_logger(debug)

    @property
    def dispatches(self) -> Dispatches:
        return Dispatches(self, self._session, self._url, self._user_agent)

    @property
    def planets(self) -> Planets:
        return Planets(self, self._session, self._url, self._user_agent)

    @property
    def status(self) -> StatusAPI:
        return StatusAPI(self, self._session, self._url, self._user_agent)

    @property
    def statistics(self) -> Statistics:
        return Statistics(self, self._session, self._url, self._user_agent)

    @property
    def war_info(self) -> WarInfoAPI:
        return WarInfoAPI(self, self._session, self._url, self._user_agent)

    @property
    def updates(self) -> UpdatesAPI:
        return UpdatesAPI(self, self._session, self._url, self._user_agent)

    @property
    def campaigns(self) -> Campaigns:
        return Campaigns(self, self._session, self._url, self._user_agent)

    @property
    def game_time(self) -> float:
        return self.status.get_status().time

    def fix_timestamp(
        self, timestamp: float, as_datetime: bool = False
    ) -> float | datetime:
        """Fixes the provided timestamp based on the current time."""

        fixed_timestamp = (time() - self.game_time) + (timestamp + self.game_time)

        return (
            datetime.fromtimestamp(fixed_timestamp) if as_datetime else fixed_timestamp
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(url={self._url})"
