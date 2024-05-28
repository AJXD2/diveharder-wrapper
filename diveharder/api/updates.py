from diveharder.api.base import ApiBase
from diveharder.objects import UpdateNews


class UpdatesAPI(ApiBase):

    def get_updates(self):
        updates = self._api_request("updates")

        for i in updates:
            yield UpdateNews.from_json(self, i)
