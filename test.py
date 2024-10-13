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
        self.assertIsInstance(assignments[0].tasks[0].data, models.AssignmentTaskData)

    def test_get_assignment(self):
        assignments = self.client.assignments.get_all_assignments()
        assignment = assignments[0]
        self.assertEqual(
            assignment, self.client.assignments.get_assignment(assignment.id)
        )

    def test_get_all_planets(self):
        planets = self.client.planets.get_planets()
        self.assertIsInstance(planets, list)
        for planet in planets:
            self._test_planet(planet)

    def _test_planet(self, planet: models.Planet):
        self.assertIsInstance(planet, models.Planet)
        self.assertIsInstance(planet.index, int)
        self.assertIsInstance(planet.name, str)
        self.assertIn(
            planet.current_owner, ["Humans", "Terminids", "Automaton", "Illuminate"]
        )

    def test_get_planet(self):
        planets = self.client.planets.get_planets()
        planet = planets[0]
        self.assertAlmostEqual(planet, self.client.planets.get_planet(planet.index))  # type: ignore
        self._test_planet(self.client.planets.get_planet(planet.index))

    def test_get_campaigns(self):
        campaigns = self.client.campaigns.get_campaigns()
        self.assertIsInstance(campaigns, list)
        self.assertTrue(len(campaigns) > 0)
        for campaign in campaigns:
            self.assertIsInstance(campaign, models.Campaign)
            self._test_campaign(campaign)

    def test_get_campaign(self):
        campaigns = self.client.campaigns.get_campaigns()
        campaign = campaigns[0]
        retrieved_campaign = self.client.campaigns.get_campaign(campaign.id)
        self.assertEqual(campaign, retrieved_campaign)
        self._test_campaign(retrieved_campaign)

    def _test_campaign(self, campaign: models.Campaign):
        self.assertIsInstance(campaign.id, int)
        self.assertIsInstance(campaign.planet, models.Planet)
        self.assertIsInstance(campaign.type, int)
        self.assertIsInstance(campaign.count, int)
        self._test_planet(campaign.planet)


if __name__ == "__main__":
    unittest.main()
