# __init__.py - Package initialization file

"""
my_package - A sample Python package demonstrating package structure.

This package contains utilities for mathematical operations, file handling,
and data processing.
"""

# Package version
__version__ = "1.0.0"
__author__ = "Python Tutorial"
__email__ = "tutorial@python.com"

# Import commonly used functions to package level
from .math_utils import add, multiply, factorial
from .file_utils import read_text_file, write_text_file
from .data_utils import DataProcessor

# Package-level constants
PACKAGE_NAME = "my_package"
SUPPORTED_FORMATS = ["txt", "csv", "json"]

# Define what gets imported with "from my_package import *"
__all__ = [
    'add', 'multiply', 'factorial',
    'read_text_file', 'write_text_file',
    'DataProcessor',
    'PACKAGE_NAME', 'SUPPORTED_FORMATS'
]

def get_package_info():
    """Return package information."""
    return {
        'name': PACKAGE_NAME,
        'version': __version__,
        'author': __author__,
        'email': __email__,
        'supported_formats': SUPPORTED_FORMATS
    }

# Package-level initialization code
print(f"Initializing {PACKAGE_NAME} v{__version__}")

# You can also perform package-level setup here
# For example: configuration loading, environment checks, etc.