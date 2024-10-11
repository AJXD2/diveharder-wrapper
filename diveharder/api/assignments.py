from diveharder.api.base import BaseApiModule
import typing
import diveharder.models as models

if typing.TYPE_CHECKING:
    from diveharder.api_client import ApiClient


class AssignmentsModule(BaseApiModule):
    """
    The Assignments API module.
    """

    def __init__(self, api_client: "ApiClient") -> None:
        super().__init__(api_client)

    def get_all_assignments(self) -> typing.List[models.Assignment]:
        """
        Gets all current assignments
        """
        data = self.get("community", "api", "v1", "assignments")
        return [models.Assignment(**assignment) for assignment in data]

    def get_assignment(self, assignment_id: int) -> models.Assignment:
        """
        Gets one assignment using the assignment ID
        """
        data = self.get("community", "api", "v1", "assignments", str(assignment_id))
        return models.Assignment(**data)
