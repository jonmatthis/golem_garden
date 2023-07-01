""" Welcome to the Garden - We're so glad you're here <3 """
__version__ = "v0.6.0"

import sys
from pathlib import Path

base_package_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path

from golem_garden.system.logging.configure_logging import configure_logging

configure_logging()
