"""Welcome to the Garden """
__version__ = "v0.4.11"
import sys
from pathlib import Path



base_package_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path
