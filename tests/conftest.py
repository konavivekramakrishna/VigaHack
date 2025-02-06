import sys
import os

"""
This code modifies the Python path to include the server directory.
It is necessary because it allows the test files to import modules from the server directory.
By adding the server directory to the Python path, we ensure that the test files can access
the application code, which is essential for running the tests.
This is useful in a project structure where the tests are located in a separate directory
from the application code, as it allows for a clean separation of concerns.
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
