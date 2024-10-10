from datetime import datetime
import logging
from time import time
import requests
from requests.adapters import HTTPAdapter, Retry


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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(url={self._url})"
