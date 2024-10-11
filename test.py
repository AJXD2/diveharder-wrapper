import unittest
from diveharder import ApiClient
from diveharder import models


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = ApiClient(
            user_agent="AJXD2",
            user_contact="aj@ajxd2.dev",
            debug=True,
            community_url="http://localhost:9090",
            diveharder_url="http://localhost:9091",
        )

    def test_get_war_info(self):
        war_info = self.client.get_war_info()
        self.assertIsInstance(war_info, models.WarInfo)

    def test_get_all_dispatches(self):
        dispatch_module = self.client.dispatch

        for i in dispatch_module.get_dispatches():
            self.assertIsInstance(i, models.Dispatch)

    def test_get_dispatch(self):
        dispatches = self.client.dispatch.get_dispatches()
        first = dispatches[-1]
        second = dispatches[0]
        self.assertEqual(first, self.client.dispatch.get_dispatch(first.id))
        self.assertEqual(second, self.client.dispatch.get_dispatch(second.id))

    def test_get_all_steam_news(self):
        steam_news = self.client.steam.get_all_steam_news()
        self.assertIsInstance(steam_news, list)
        self.assertIsInstance(steam_news[0], models.SteamNews)

    def test_get_steam_news(self):
        data = self.client.steam.get_all_steam_news()
        testing_id = data[0].id
        steam_news = self.client.steam.get_steam_news(testing_id)
        self.assertIsInstance(steam_news, models.SteamNews)

    def test_get_all_assignments(self):
        assignments = self.client.assignments.get_all_assignments()

        self.assertIsInstance(assignments, list)
        self.assertIsInstance(assignments[0], models.Assignment)
        self.assertIsInstance(assignments[0].id, int)
        self.assertIsInstance(assignments[0].tasks, list)
        self.assertIsInstance(assignments[0].tasks[0], models.AssignmentTask)
        self.assertIsInstance(assignments[0].tasks[0].data, dict)

    def test_get_assignment(self):
        assignments = self.client.assignments.get_all_assignments()
        assignment = assignments[0]
        self.assertEqual(
            assignment, self.client.assignments.get_assignment(assignment.id)
        )


if __name__ == "__main__":
    unittest.main()
