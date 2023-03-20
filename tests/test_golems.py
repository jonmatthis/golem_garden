from golem_garden.context_database import ContextDatabase
from golem_garden.golems import Golem, GreeterGolem, GardenerGolem, ExpertGolem


def test_golem_instantiation():
    golem = Golem(name="Test Golem",
                  type="test",
                  context_database=ContextDatabase(),
                  golem_string="test_string",
                  model="test_model")
    assert golem.name == "Test Golem"
    assert golem.type == "test"
    assert golem.golem_string == "test_string"
    assert golem.model == "test_model"


def test_greeter_golem_instantiation():
    greeter_golem = GreeterGolem(name="Test Golem",
                  type="greeter",
                  context_db=ContextDatabase(),
                  golem_string="test_string",
                  model="test_model")
    assert isinstance(greeter_golem, GreeterGolem)
    assert isinstance(greeter_golem, Golem)


def test_gardener_golem_instantiation():
    gardener_golem = GardenerGolem(name="Test Golem",
                  type="gardener",
                  context_db=ContextDatabase(),
                  golem_string="test_string",
                  model="test_model")
    assert isinstance(gardener_golem, GardenerGolem)
    assert isinstance(gardener_golem, Golem)


def test_expert_golem_instantiation():
    expert_golem = ExpertGolem(name="Test Golem",
                  type="expert",
                  context_db=ContextDatabase(),
                  golem_string="test_string",
                  model="test_model")
    assert isinstance(expert_golem, ExpertGolem)
    assert isinstance(expert_golem, Golem)
