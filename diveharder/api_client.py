import logging
import requests
from requests.adapters import HTTPAdapter, Retry
from diveharder.constants import OFFICIAL_DIVEHARDER_URL, OFFICIAL_COMMUNITY_URL
from diveharder.models import APIURLConfiguration


def retry_adapter(
    backoff_factor: float, retries: int, extra_retry_codes: list = []
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


def set_logger() -> logging.Logger:
    """Configures debug logging if requested."""
    from rich.logging import RichHandler

    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    logger.addHandler(
        RichHandler(
            level=logging.DEBUG,
            omit_repeated_times=False,
            markup=True,
            rich_tracebacks=True,
            log_time_format="%X %p",
        )
    )
    return logger


class ApiClient:
    """
    The client used to interact with the Helldivers 2 APIs
    """

    def __init__(
        self,
        user_agent: str = None,
        debug: bool = None,
        diveharder_url: str = None,
        community_url: str = None,
    ) -> None:
        """The client used to interact with the Helldivers 2 APIs

        Args:
            user_agent (str, optional): The user agent to use when making requests. Defaults to "Helldivers2APIUser".
            debug (bool, optional): Enables debug logging for development. Defaults to False.
            diveharder_url (str, optional): The diveharder API url to use. Defaults to `constants.OFFICIAL_DIVEHARDER_URL`.
            community_url (str, optional): The community API url to use. Defaults to `constants.OFFICIAL_COMMUNITY_URL`.
        """
        self.logger = set_logger() if debug else None
        self.api_config = APIURLConfiguration(
            diveharder=diveharder_url or OFFICIAL_DIVEHARDER_URL,
            community=community_url or OFFICIAL_COMMUNITY_URL,
        )
        self._user_agent = user_agent
        self._setup_session()

    def _setup_session(self):
        self._session = requests.Session()
        self._session.mount("https://", retry_adapter(0.2, 5))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(url={self._url})"
