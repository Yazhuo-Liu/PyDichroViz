import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pprint
from module.crystal.loader import CrystalStructureLoader
from module.slab.builder import build_slab_structure
from module.slab.visualize_slab import visualize_slab_layers

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