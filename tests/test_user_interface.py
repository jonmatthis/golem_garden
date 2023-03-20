# test_user_interface.py

import asyncio
import unittest
from unittest.mock import patch

from golem_garden.golem_garden import GolemGarden
from golem_garden.golems import GreeterGolem
from golem_garden.user_interface import UserInterface


class TestUserInterface(unittest.TestCase):
    def setUp(self):
        self._golem_garden = GolemGarden()
        self._user_interface = UserInterface(self._golem_garden)
        self._user_interface.run()

    def test_user_interface(self):
        with patch('builtins.input', side_effect=["Hello", "quit"]), \
             patch('builtins.print') as mock_print:
            asyncio.run(self._user_interface.start())

            printed_messages = [call[0][0] for call in mock_print.call_args_list]
            self.assertTrue(len(printed_messages) > 0)
