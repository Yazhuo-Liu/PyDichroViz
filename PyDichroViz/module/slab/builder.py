import numpy as np
from ..crystal.loader import CrystalStructureLoader

Array2D = np.ndarray  # shape: (N, 2), representing N atoms with x, y


def build_slab_structure(
    crystal_data: dict,
    a: float = 1.0,
    repeat_x: int = 3,
    repeat_y: int = 3
) -> np.ndarray:
    """
    Build a 2D slab by repeating the unit cell in-plane and stacking layers,
    centered around the origin.

    Args:
        crystal_data (dict): Parsed crystal data from CrystalStructureLoader.
        a (float): Lattice constant.
        repeat_x (int): Number of repetitions along x-direction (total, centered).
        repeat_y (int): Number of repetitions along y-direction (total, centered).

    Returns:
        np.ndarray: A 3D NumPy array of shape (num_layers, num_atoms_per_layer, 2).
    """
    # Step 0: Read number of layers from crystal_data
    if "layers_per_supercell" not in crystal_data:
        raise KeyError("Required field 'layers_per_supercell' is missing in crystal data.")

    num_layers = crystal_data["layers_per_supercell"]
    if not isinstance(num_layers, int) or num_layers < 1:
        raise ValueError(f"'layers_per_supercell' must be a positive integer. Got: {num_layers}")

    # Step 1: Extract lattice basis and offsets
    basis_positions = np.array(crystal_data["basis"]["positions"]) * a
    in_plane_offsets = np.array(crystal_data["in_plane_offsets"]) * a

    x_period = crystal_data.get("x_period", crystal_data["periods"]["x"]) * a
    y_period = crystal_data.get("y_period", crystal_data["periods"]["y"]) * a

    num_basis = len(basis_positions)

    # Step 2: Generate symmetric x/y repetitions around 0
    x_half = repeat_x // 2
    y_half = repeat_y // 2

    # If repeat_x/y is odd, include 0, otherwise center symmetrically
    x_indices = np.arange(-x_half, x_half + 1) if repeat_x % 2 else np.arange(-x_half, x_half)
    y_indices = np.arange(-y_half, y_half + 1) if repeat_y % 2 else np.arange(-y_half, y_half)

    xx, yy = np.meshgrid(x_indices, y_indices, indexing='ij')
    shifts = np.stack([xx.ravel(), yy.ravel()], axis=1) * [x_period, y_period]

    # Broadcast basis positions across all tiles
    tile_shifts = np.repeat(shifts[np.newaxis, :, :], num_basis, axis=0)
    tiled_basis = np.repeat(basis_positions[:, np.newaxis, :], len(shifts), axis=1)

    atoms_in_unit = (tiled_basis + tile_shifts).reshape(-1, 2)

    # Step 3: Stack layers with offsets
    layer_offsets = np.tile(in_plane_offsets, (num_layers, 1))[:num_layers]
    slab_array = atoms_in_unit + layer_offsets[:, np.newaxis, :]

    return slab_array