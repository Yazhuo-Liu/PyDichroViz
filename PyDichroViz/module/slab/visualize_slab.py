import matplotlib.pyplot as plt
from typing import Optional, List, Union, Tuple
import numpy as np
import os
from ..crystal.loader import CrystalStructureLoader
from .builder import build_slab_structure


def visualize_slab_layers(
    slab_array: np.ndarray,
    markers: Union[str, List[str]] = "auto",
    colors: Union[str, List[str]] = "auto",
    size: int = 50,
    labels: Optional[List[str]] = None,
    title: str = "Slab Structure Layers",
    show: bool = True,
    output_path: Optional[str] = None
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Visualize the slab structure layer by layer using different markers and colors.

    Args:
        slab_array (np.ndarray): Output from build_slab_structure, shape (L, N, 2).
        markers (Union[str, List[str]]): Marker style for each layer.
        colors (Union[str, List[str]]): Color for each layer.
        size (int): Size of the plotted points.
        labels (Optional[List[str]]): Layer labels for legend.
        title (str): Plot title.
        show (bool): Whether to call plt.show().
        output_path (Optional[str]): If provided, save figure to this path.

    Returns:
        fig, ax: Matplotlib figure and axes objects.
    """
    # Input validation
    if not isinstance(slab_array, np.ndarray):
        raise ValueError("Expected 'slab_array' to be a NumPy array.")
    if slab_array.ndim != 3 or slab_array.shape[-1] != 2:
        raise ValueError("slab_array must be a 3D array with shape (L, N, 2).")

    num_layers = slab_array.shape[0]

    # Default marker and colors
    default_markers = ['o', 's', '^', 'D', 'v', '>', '<', 'p', '*', 'X', 'P']
    default_colors = plt.cm.tab10(np.linspace(0, 1, num_layers))

    if markers == "auto":
        markers = [default_markers[i % len(default_markers)] for i in range(num_layers)]
    elif isinstance(markers, list):
        assert len(markers) >= num_layers, "Not enough markers provided for all layers."
    else:
        raise ValueError("markers must be 'auto' or a list of strings.")

    if colors == "auto":
        colors = [default_colors[i % len(default_colors)] for i in range(num_layers)]
    elif isinstance(colors, list):
        assert len(colors) >= num_layers, "Not enough colors provided for all layers."
    else:
        raise ValueError("colors must be 'auto' or a list of strings.")

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))

    for i in range(num_layers):
        layer_atoms = slab_array[i]
        label = labels[i] if labels else f"Layer {i}"
        ax.scatter(
            layer_atoms[:, 0], layer_atoms[:, 1],
            c=[colors[i]],
            marker=markers[i],
            s=size,
            label=label,
            edgecolor='black'
        )

    ax.set_title(title)
    ax.set_xlabel("x (Å)")
    ax.set_ylabel("y (Å)")
    ax.set_aspect('equal')

    if labels or title:
        ax.legend()

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        print(f"Saving plot to {output_path}")
        fig.savefig(output_path, dpi=150, bbox_inches='tight')

    if show:
        plt.tight_layout()
        plt.show()

    return fig, ax


# ================================================
# Test Case (Main Guard)
# ================================================

if __name__ == "__main__":
    import pprint

    pp = pprint.PrettyPrinter(indent=2)

    print("Running test inside visualize_slab.py")

    # Step 1: Load crystal data
    loader = CrystalStructureLoader("fcc", "110")
    try:
        crystal_data = loader.load_structure()
        print("Successfully loaded crystal structure:")
        pp.pprint(crystal_data["_meta"])
    except Exception as e:
        print(f"Failed to load crystal: {e}")
        exit(1)

    # Step 2: Build slab
    print("\nBuilding slab...")
    try:
        slab = build_slab_structure(
            crystal_data=crystal_data,
            a=1.0,
            repeat_x=20,
            repeat_y=20
        )
        print(f"\nSlab built successfully. Shape: {slab.shape} → (layers, atoms per layer, coordinates)")
    except Exception as e:
        print(f"Error during slab building: {e}")
        exit(1)

    # Step 3: Visualize and save
    system = crystal_data["_meta"]["crystal_system"]
    plane = crystal_data["_meta"]["plane"]

    output_dir = "output"
    output_file = os.path.join(output_dir, f"slab_{system}_{plane}.png")

    print("\nVisualizing and saving plot...")
    visualize_slab_layers(
        slab,
        markers="auto",
        colors="auto",
        size=50,
        labels=[f"Layer {i}" for i in range(slab.shape[0])],
        title=f"{system.upper()}({plane}) Slab",
        show=True,
        output_path=output_file
    )

    print("Visualization completed.")
