"""
Data schemas and validation for crystal structures
"""

from typing import List
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

class CrystalBasis(BaseModel):
    """Atomic basis positions in unit cell"""
    positions: List[List[float]] = Field(..., min_length=2, max_length=2)

class CrystalPlaneData(BaseModel):
    """Data structure for a specific crystal plane"""
    basis: CrystalBasis
    lattice_constant: float = 1.0
    layers_per_supercell: int
    in_plane_offsets: List[List[float]] = Field(..., min_length=2, max_length=2)
    out_of_plane_offsets: List[float]
    x_period: int = 1
    y_period: int = 1

    @field_validator('in_plane_offsets')
    @classmethod
    def validate_in_plane_offsets(cls, v: List[List[float]], info: ValidationInfo):
        if len(v) != info.data['layers_per_supercell']:
            raise ValueError("Number of in-plane offsets must match layers_per_supercell")
        return v

    @field_validator('out_of_plane_offsets')
    @classmethod
    def validate_out_of_plane_offsets(cls, v: List[float], info: ValidationInfo):
        if len(v) != info.data['layers_per_supercell']:
            raise ValueError("Number of out-of-plane offsets must match layers_per_supercell")
        return v