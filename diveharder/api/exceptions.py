# Base class for exceptions
class DiveharderApiException(Exception):
    """Base class for exceptions in this module."""

    pass


class BadRequestError(DiveharderApiException):
    """Raised when a bad request is made."""

    pass


class DiveHarderApiError(DiveharderApiException):
    """Raised when an error is returned from the API."""

    pass
