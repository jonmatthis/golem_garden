# test_golem_factory.py

import unittest

from golem_garden.context_database import ContextDatabase
from golem_garden.golems.golem_factory import GolemFactory
from golem_garden.golems.golem import GreeterGolem, GardenerGolem, ExpertGolem

class TestGolemFactory(unittest.TestCase):
    def setUp(self):
        self.golem_factory = GolemFactory(context_database=ContextDatabase())

    def test_create_golem(self):
        greeter_golem = self.golem_factory.create_golem("GreeterGolem")
        self.assertIsInstance(greeter_golem, GreeterGolem)

        gardener_golem = self.golem_factory.create_golem("GardenerGolem")
        self.assertIsInstance(gardener_golem, GardenerGolem)

        sub_golem = self.golem_factory.create_golem("ExpertGolem")
        self.assertIsInstance(sub_golem, ExpertGolem)

        with self.assertRaises(KeyError):
            self.golem_factory.create_golem("InvalidGolem")
