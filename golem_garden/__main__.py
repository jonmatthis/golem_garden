import logging
import sys
from pathlib import Path

from golem_garden.view_layer.command_line_interface.cli import main

base_package_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path

from rich.console import Console

from golem_garden.data_model_layer.system.logging.configure_logging import configure_logging

configure_logging()

rich_console = Console()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    main()
