import pytest
import os
import sys
import warnings

# Filter out the specific deprecation warning
warnings.filterwarnings("ignore", message=".*jsonschema.RefResolver is deprecated.*")

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 