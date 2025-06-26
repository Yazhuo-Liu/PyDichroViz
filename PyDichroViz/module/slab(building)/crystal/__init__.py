"""
Crystal Data Generation Module

This module provides functionality to generate atomic position data 
for creating dichromatic diagrams.

"""

from .core import CrystalDataGenerator, generate_atomic_positions
from .exceptions import CrystalDataError, InvalidCrystalType

__all__ = [
    'CrystalDataGenerator',
    'generate_atomic_positions',
    'CrystalDataError',
    'InvalidCrystalType'
]

__version__ = '0.1.0'