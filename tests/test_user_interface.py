# test_user_interface.py

import asyncio
import unittest
from unittest.mock import patch
from golem_garden.golems import GreeterGolem

class TestUserInterface(unittest.TestCase):
    def setUp(self):
        self.greeter_golem = GreeterGolem("Greeter Golem", "greeter")
        self.user_interface = UserInterface(self.greeter_golem)

    def test_user_interface(self):
        with patch('builtins.input', side_effect=["Hello", "quit"]), \
             patch('builtins.print') as mock_print:
            asyncio.run(self.user_interface.start())

            printed_messages = [call[0][0] for call in mock_print.call_args_list]
            self.assertTrue(len(printed_messages) > 0)
