# test_golem_factory.py


class TestGolemFactory(unittest.TestCase):
    def setUp(self):
        self.golem_factory = GolemFactory(context_database=ContextDatabase())

    def test_create_golem(self):
        test_golem = self.golem_factory.create_golem("Golem")
        self.assertIsInstance(test_golem, Golem)

