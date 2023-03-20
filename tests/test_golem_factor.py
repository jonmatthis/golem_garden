# test_golem_factory.py

import unittest
from golem_garden.golem_factory import GolemFactory
from golem_garden.golems import GreeterGolem, GardenerGolem, SubGolem

class TestGolemFactory(unittest.TestCase):
    def setUp(self):
        self.golem_factory = GolemFactory()

    def test_create_golem(self):
        greeter_golem = self.golem_factory.create_golem("GreeterGolem")
        self.assertIsInstance(greeter_golem, GreeterGolem)

        gardener_golem = self.golem_factory.create_golem("GardenerGolem")
        self.assertIsInstance(gardener_golem, GardenerGolem)

        sub_golem = self.golem_factory.create_golem("SubGolem")
        self.assertIsInstance(sub_golem, SubGolem)

        with self.assertRaises(KeyError):
            self.golem_factory.create_golem("InvalidGolem")
