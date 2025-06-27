# module/csl/__init__.py

import sys
from .csl_generator import main
from .csl_generator import sigma_list, calculate_GB_planes

# Define what should be exposed when someone uses: from crystal import *
__all__ = [
    "main",                   # Main function for generating CSL files
    "sigma_list",              # Function for printing lists in a formatted way
    "calculate_GB_planes"      # Function for calculating grain boundary planes
]

if __name__ == "__main__":
    sys.exit(main())