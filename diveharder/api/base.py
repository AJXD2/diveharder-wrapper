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
        mode="GET",
        params=None,
        data=None,
        json=None,
        override_headers=None,
        data_as_json=True,
        includes=None,
        raw=False,
    ):
        """Make a request to the DiveHarder API.

        Args:
            endpoint(str): URI for the API
            mode(str): Request type, one of ('GET', 'POST', 'PATCH',
                    'DELETE', 'PUT')
            params(dict): Extra parameters to pass to the endpoint,
                    e.g. a query string
            data(dict): POST data
            json(bool): Set to False to return the response object,
                    True for just JSON.  Defaults to returning JSON if possible
                    otherwise the response object.
            override_headers(dict): Headers to override, e.g. to set the
                    Content-Type
            data_as_json(bool): If True data will be posted as JSON
            includes(iter): List of includes to be added as a param,
                    e.g. ('servers', 'users')

        Returns:
            response: A HTTP response object or the JSON response depending on
                    the value of the json parameter.
        """
        if not endpoint:
            raise BadRequestError("No API endpoint was specified.")
        if raw:
            url = url_join(self._url, "raw", endpoint)
        else:
            url = url_join(self._url, "v1", endpoint)
        headers = self._get_headers()
        if override_headers:
            headers.update(override_headers)

        if includes:
            include_str = ",".join(includes)
            if params and params.get("include"):
                params["include"] += "," + include_str
            elif params:
                params["include"] = include_str
            else:
                params = {"include": include_str}

        if mode == "GET":
            response = self._session.get(url, params=params, headers=headers)
        elif mode == "POST":
            if data_as_json:
                response = self._session.post(
                    url, params=params, headers=headers, json=data
                )
            else:
                response = self._session.post(
                    url, params=params, headers=headers, data=data
                )
        elif mode == "PATCH":
            response = self._session.patch(
                url, params=params, headers=headers, json=data
            )
        elif mode == "DELETE":
            response = self._session.delete(url, params=params, headers=headers)
        elif mode == "PUT":
            response = self._session.put(url, params=params, headers=headers, json=data)
        else:
            raise BadRequestError(
                "Invalid request type specified(%s).  Must be one of %r."
                % (mode, REQUEST_TYPES)
            )

        try:
            response_json = response.json()
        except ValueError:
            response_json = {}

        if response.status_code in (400, 422):
            raise DiveHarderApiError(
                "API Request resulted in errors: %s" % response_json.get("errors")
            )
        else:
            response.raise_for_status()

        if json is True:
            return response_json
        elif json is False:
            return response
        else:
            return response_json or response

    @property
    def client(self):
        return self._client
