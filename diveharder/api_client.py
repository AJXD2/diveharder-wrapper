from functools import lru_cache
import requests
import requests.adapters
import logging
from diveharder.api.campaings import Campaigns
from diveharder.api.dispatches import Dispatches
from diveharder.api.planets import Planets
from diveharder.api.status import StatusAPI
from diveharder.constants import OFFICIAL_DIVEHARDER_URL, __version__
from diveharder.utils import url_join


def retry_adapter(backoff_factor, retries, extra_retry_codes):
    """Configures an HTTP adapter with retries and backoff."""
    retry_codes = [429] + extra_retry_codes
    retries = requests.adapters.Retry(
        total=retries,
        status_forcelist=retry_codes,
        backoff_factor=backoff_factor,
        allowed_methods=["DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT"],
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retries)

    return adapter


def set_logger(debug):
    """Configure debug logging if requested."""
    if debug:
        level = logging.DEBUG
    else:
        level = logging.ERROR

    logging.basicConfig()
    logging.getLogger().setLevel(level)
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.propagate = True


class DiveHarderApiClient:
    def __init__(
        self,
        user_agent: str = "DiveHarderAPIWrapper/" + __version__,
        url: str = OFFICIAL_DIVEHARDER_URL,
        retry_count: int = 5,
        backoff_factor: float = 0.2,
        debug: bool = False,
    ) -> None:
        self._url = url
        self._session = requests.Session()
        self._session.mount("https://", retry_adapter(backoff_factor, retry_count, []))
        self._session.mount("http://", retry_adapter(backoff_factor, retry_count, []))
        self._user_agent = user_agent
        set_logger(debug)

    @property
    def dispatches(self):
        return Dispatches(self, self._session, self._url, self._user_agent)

    @property
    def planets(self):
        return Planets(self, self._session, self._url, self._user_agent)

    @property
    def status(self):
        return StatusAPI(self, self._session, self._url, self._user_agent)

    @property
    def campaigns(self):
        return Campaigns(self, self._session, self._url, self._user_agent)

    @property
    @lru_cache(maxsize=1)
    def all(self):
        return self._session.get(url_join(self._url, "v1", "all")).json()

    @property
    def current_time(self):
        data = self.all
        start_date = data.get("war_info", {}).get("startDate", 0)
        now = data.get("status", {}).get("time", 0)

        return start_date + now

    def fix_timestamp(self, timestamp: float):
        # Epoch Start time + War Start Date + Time

        return self.current_time + timestamp

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(url={self._url})"
