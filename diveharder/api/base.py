from diveharder.api.exceptions import BadRequestError, DiveHarderApiError
from diveharder.constants import REQUEST_TYPES
from diveharder.utils import url_join


class ApiBase:

    def __init__(
        self,
        client: any,
        session: str,
        url: str,
        client_agent: str,
    ):
        from diveharder.api_client import DiveHarderApiClient

        self._client: DiveHarderApiClient = client
        self._session = session
        self._url = url
        self._client_agent = client_agent

    def _get_headers(self):
        return {
            "Accept": "application/json",
            "X-Super-Client": self._client_agent,
            "Content-Type": "application/json",
        }

    def _api_request(
        self,
        endpoint,
        method="GET",
        params=None,
        data=None,
        json=None,
        headers=None,
        includes=None,
        raw=False,
    ):
        """Make a request to the DiveHarder API."""

        if not endpoint:
            raise BadRequestError("No API endpoint was specified.")

        url = url_join(self._url, "raw" if raw else "v1", endpoint)
        headers = self._get_headers()
        if headers and headers.get("Content-Type"):
            headers["Content-Type"] = "application/json"
        if headers and headers.get("Accept"):
            headers["Accept"] = "application/json"
        if headers and headers.get("X-Super-Client"):
            headers["X-Super-Client"] = self._client_agent
        if headers and headers.get("override_headers"):
            headers.update(headers.pop("override_headers"))

        if includes:
            include_str = ",".join(includes)
            params = params or {}
            params["include"] = include_str

        method_mapping = {
            "GET": self._session.get,
            "POST": self._session.post,
            "PATCH": self._session.patch,
            "DELETE": self._session.delete,
            "PUT": self._session.put,
        }
        request_method = method_mapping.get(method)
        if not request_method:
            raise BadRequestError(f"Invalid request type: {method}")

        response = request_method(url, params=params, headers=headers, json=data)
        try:
            response_json = response.json()
        except ValueError:
            response_json = {}

        if response.status_code in (400, 422):
            raise DiveHarderApiError(response_json.get("errors"))

        response.raise_for_status()

        if json is False:
            return response
        return response_json

    @property
    def client(self):
        return self._client
