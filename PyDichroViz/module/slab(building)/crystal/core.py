"""
Core functionality for crystal data generation
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from .exceptions import InvalidCrystalType, DataValidationError, DataNotFoundError
from .schemas import CrystalPlaneData

class CrystalDataGenerator:
    """
    Generator for atomic position data used in two-color diagrams
    
    Features:
    1. Loads crystal structure data from organized JSON files
    2. Generates atomic positions with scaling and supercell support
    3. Validates crystal data structure
    """
    
    def __init__(self, data_dir: str = "crystal_data"):
        """
        Initialize the generator with data directory
        
        Args:
            data_dir: Path to directory containing crystal data
        """
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise DataNotFoundError(f"Crystal data directory {data_dir} not found")
    
    def load_crystal_data(self, 
                         crystal_type: str, 
                         plane: str) -> Dict:
        """
        Load crystal data for specified type and plane
        
        Args:
            crystal_type: Crystal structure type (e.g., 'fcc', 'bcc')
            plane: Miller indices of plane (e.g., '111', '100')
            
        Returns:
            Dictionary containing crystal data
            
        Raises:
            InvalidCrystalType: If crystal/plane combination doesn't exist
            DataValidationError: If loaded data fails validation
        """
        crystal_type = crystal_type.lower()
        plane = plane.lower()
        file_path = self.data_dir / crystal_type / f"{plane}.json"
        
        if not file_path.exists():
            raise InvalidCrystalType(
                f"No data found for {crystal_type} {plane}"
            )
        
        try:
            with open(file_path, 'r') as f:
                raw_data = json.load(f)
            
            # Validate data structure
            try:
                plane_data = CrystalPlaneData(**raw_data)
                return plane_data.dict()
            except Exception as e:
                raise DataValidationError(
                    f"Invalid data structure in {file_path}: {str(e)}"
                )
                
        except (json.JSONDecodeError, IOError) as e:
            raise DataValidationError(
                f"Error reading {file_path}: {str(e)}"
            )
    
    def generate_atomic_positions(self,
                                 crystal_type: str,
                                 plane: str,
                                 lattice_constant: float = 1.0,
                                 supercell_size: Tuple[int, int, int] = (1, 1, 1)) -> Dict:
        """
        Generate atomic position data for two-color diagram
        
        Args:
            crystal_type: Crystal structure type
            plane: Miller indices of plane
            lattice_constant: Lattice constant in angstroms
            supercell_size: Supercell dimensions (nx, ny, nz)
            
        Returns:
            Dictionary containing:
            - atomic_positions: List of [x,y,z] positions
            - x_period: Periodicity in x-direction
            - y_period: Periodicity in y-direction
            - layers: Number of layers in supercell
            - in_plane_offsets: Offsets for each layer
            - out_of_plane_offsets: Z-offsets for each layer
        """
        # Load base data
        base_data = self.load_crystal_data(crystal_type, plane)
        
        # Scale positions by lattice constant
        scale_factor = lattice_constant / base_data['lattice_constant']
        scaled_basis = [
            [x*scale_factor, y*scale_factor, z*scale_factor]
            for x, y, z in base_data['basis']['positions']
        ]
        
        # Scale out-of-plane offsets
        scaled_offsets = [
            z*scale_factor 
            for z in base_data['out_of_plane_offsets']
        ]
        
        # Create supercell
        nx, ny, nz = supercell_size
        atomic_positions = []
        
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    for atom in scaled_basis:
                        new_pos = [
                            atom[0] + i,
                            atom[1] + j,
                            atom[2] + k
                        ]
                        atomic_positions.append(new_pos)
        
        # Prepare output data
        return {
            'atomic_positions': atomic_positions,
            'x_period': nx * base_data['x_period'],
            'y_period': ny * base_data['y_period'],
            'layers': nz * base_data['layers_per_supercell'],
            'in_plane_offsets': base_data['in_plane_offsets'],
            'out_of_plane_offsets': scaled_offsets,
            'crystal_type': crystal_type,
            'plane': plane,
            'lattice_constant': lattice_constant,
            'supercell_size': supercell_size
        }
    
    def list_available_crystals(self) -> Dict[str, List[str]]:
        """
        List all available crystal types and planes
        
        Returns:
            Dictionary {crystal_type: [list_of_planes]}
        """
        available = {}
        for crystal_dir in self.data_dir.iterdir():
            if crystal_dir.is_dir():
                crystal_type = crystal_dir.name
                planes = [
                    f.stem for f in crystal_dir.glob('*.json')
                    if f.is_file()
                ]
                if planes:
                    available[crystal_type] = planes
        return available

def generate_atomic_positions(crystal_type: str,
                            plane: str,
                            **kwargs) -> Dict:
    """
    Convenience function to generate atomic positions
    
    Args:
        crystal_type: Crystal structure type
        plane: Miller indices of plane
        kwargs: Additional arguments (lattice_constant, supercell_size)
        
    Returns:
        Atomic position data dictionary
    """
    generator = CrystalDataGenerator()
    return generator.generate_atomic_positions(crystal_type, plane, **kwargs)