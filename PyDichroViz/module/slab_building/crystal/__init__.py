# module/slab_building/crystal/__init__.py

"""
Package initialization for the 'crystal' module.

This file initializes the package and exposes key classes to make them
easily accessible to external modules.
"""

# Import main classes from submodules
from .parser import CrystalDataParser
from .loader import CrystalStructureLoader

# Define what should be exposed when someone uses: from crystal import *
__all__ = [
    "CrystalDataParser",     # Class for parsing crystal structure JSON files
    "CrystalStructureLoader" # Class for loading and validating crystal structures based on system and plane
]