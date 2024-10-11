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
        print("War Info:")
        print("\tTime:")
        print(f"\t  Started: {war_info.started}")
        print(f"\t  Now: {war_info.now}")
        print(f"\t  Ended: {war_info.ended}")
        print("\tFactions:")
        for i in war_info.factions:
            print(f"\t  - {i}")
        print(f"\tImpact Mult: {war_info.impact_multiplier}")
        print("\tStatistics:")
        for k, v in war_info.statistics.model_dump().items():
            print(f"\t  - {k}: {v}")

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
