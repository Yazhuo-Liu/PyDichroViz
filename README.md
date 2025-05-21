# PyDichroViz: A Python Library for Dichromatic Pattern and CSL Visualization

## Introduction

`PyDichroViz` is an open-source Python library designed to help materials scientists and researchers visualize grain boundaries through dichromatic patterns and Coincidence Site Lattice (CSL) theory. It provides tools to calculate and plot the atomic arrangements of two misoriented crystals, highlighting the coincident sites, which are crucial for understanding grain boundary structures and properties.

## Project Status
This project is currently in its early stages of development and is actively under construction. We are building the core functionalities and welcome contributions and feedback from the community.

## Core Goals

This library aims to achieve the following core objectives:

1.  **Accurate CSL Calculation and Visualization**: Precisely calculate and visualize the Coincidence Site Lattice (CSL) based on user-defined crystal structures and relative orientations.
2.  **High-Quality Dichromatic Pattern Generation**: Provide intuitive and clear 2D and 3D dichromatic plots to illustrate the relative positions and coincidence patterns of two crystals.
3.  **Support for Common Crystal Structures**: Handle various crystal systems, including Cubic (FCC, BCC) and Hexagonal (HCP).
4.  **Flexible Parameter Customization**: Allow users to customize plot parameters such as crystal colors, coincidence point colors, atom sizes, and projection planes to suit different analysis and presentation needs.
5.  **User-Friendliness**: Offer a concise API interface and clear documentation to facilitate quick adoption and ease of use.

## Module Breakdown and Functional Logic

To achieve the above goals, the project is divided into the following core modules:

### 1. `crystallography` Module (Crystallography Fundamentals)

This module handles the basic definition and manipulation of crystal structures.

* **`Crystal` Class**:
    * **Attributes**:
        * `lattice_vectors`: Lattice basis vectors (e.g., a $3 \times 3$ NumPy array).
        * `basis_atoms`: Positions of basis atoms within the unit cell (fractional or Cartesian coordinates) and element type (e.g., `[[x, y, z, 'Fe'], ...]`).
        * `crystal_system`: Crystal system (e.g., 'cubic', 'hexagonal'), for internal validation or specific system handling.
        * `lattice_parameters`: Lattice parameters (a, b, c, $\alpha$, $\beta$, $\gamma$).
    * **Methods**:
        * `from_lattice_parameters(a, b, c, alpha, beta, gamma, basis_atoms)`: Defines a crystal from lattice parameters and basis atoms.
        * `generate_unit_cell_points()`: Generates all atom positions within a single unit cell (Cartesian coordinates).
        * `generate_supercell_points(n_x, n_y, n_z)`: Generates all atom positions within a specified supercell size.
        * `rotate(rotation_matrix)`: Rotates the crystal based on a given rotation matrix (updates its internal lattice vectors and atom positions).
        * `translate(translation_vector)`: Translates the crystal.

### 2. `csl_calculator` Module (Coincidence Site Lattice Calculation)

This module is the core computational part of the project, responsible for identifying coincident points and calculating $\Sigma$ values.

* **`CSLCalculator` Class**:
    * **Attributes**:
        * `crystal1`: The first `Crystal` object.
        * `crystal2`: The second `Crystal` object.
        * `tolerance`: Distance tolerance for determining if two atom positions coincide (float).
    * **Methods**:
        * `set_relative_orientation(rotation_matrix, translation_vector=None)`: Sets the rotation and translation relationship of `crystal2` relative to `crystal1`.
        * `find_coincidence_points(supercell_size)`:
            * Takes the supercell dimensions (e.g., `[Nx, Ny, Nz]`).
            * Generates atom point sets for both crystals' supercells.
            * Transforms `crystal2`'s atom points according to the set rotation and translation.
            * **Core Algorithm**: Uses an efficient nearest-neighbor search algorithm (e.g., `scipy.spatial.KDTree`) to find pairs of atoms that coincide within the `tolerance`.
            * Returns a list of all coincident point coordinates, along with a list indicating which points belong to Crystal 1, Crystal 2, and which are coincident.
        * `calculate_sigma_value()`: (Optional but recommended) Calculates the theoretical $\Sigma$ value based on the input rotation matrix. This requires some crystallographic mathematical knowledge, such as finding the least common multiple volume corresponding to the rotation matrix.

### 3. `dichromatic_plotter` Module (Plotting)

This module is responsible for visualizing the calculated results as dichromatic patterns.

* **`DichromaticPlotter` Class**:
    * **Attributes**:
        * `crystal1_points`: List of atom coordinates for Crystal 1.
        * `crystal2_points`: List of atom coordinates for Crystal 2.
        * `coincidence_points`: List of coordinates for coincident atoms.
        * `plot_settings`: Dictionary of plotting parameters (e.g., `{'color1': 'blue', 'color2': 'red', 'coincidence_color': 'green', 'marker_size': 5, 'alpha': 0.8}`).
    * **Methods**:
        * `plot_2d(plane_normal, thickness=None, ax=None)`:
            * Projects atoms onto a specified 2D plane (e.g., `[0,0,1]` for projection onto the xy-plane).
            * An optional `thickness` parameter can be set to display atoms only within that thickness range.
            * Uses `matplotlib.pyplot` to create a scatter plot.
            * Assigns different colors and markers based on atom type (Crystal 1, Crystal 2, coincident).
            * Adds axis labels, title, legend, etc.
        * `plot_3d(ax=None)`:
            * Uses `matplotlib.axes.Axes3D` or `plotly.graph_objects` to create a 3D scatter plot.
            * Provides interactive rotation and zooming (if using Plotly).
            * Similarly assigns colors and markers based on atom type.

### 4. `utils` Module (Utility Functions)

This module will contain various general-purpose helper functions.

* **`rotation_matrices`**:
    * `euler_to_rotation_matrix(alpha, beta, gamma)`: Converts Euler angles to a rotation matrix.
    * `axis_angle_to_rotation_matrix(axis, angle_deg)`: Converts axis-angle representation to a rotation matrix.
* **`unit_cell_generators`**:
    * `fcc_unit_cell(a)`: Generates unit cell basis vectors and basis atoms for an FCC crystal.
    * `bcc_unit_cell(a)`: Generates unit cell basis vectors and basis atoms for a BCC crystal.
    * `hcp_unit_cell(a, c)`: Generates unit cell basis vectors and basis atoms for an HCP crystal.
    * ... (More common crystal structures can be added as needed)
* **`transformations`**:
    * `cartesian_to_fractional(coords, lattice_vectors)`: Converts Cartesian coordinates to fractional coordinates.
    * `fractional_to_cartesian(coords, lattice_vectors)`: Converts fractional coordinates to Cartesian coordinates.

## Technology Stack

* **Core Language**: Python
* **Numerical Computation**: `NumPy` (for handling vectors, matrices, and atom coordinates)
* **Scientific Computing**: `SciPy` (specifically `scipy.spatial.KDTree` for efficient nearest-neighbor search, and potential rotation matrix operations)
* **Plotting**:
    * **2D Static Plots**: `Matplotlib` (standard library, powerful)
    * **3D Interactive Plots (Optional)**: `Plotly` (for high-quality interactive web charts) or `Mayavi` (if the user has a VTK environment)
* **Project Management**: `Poetry` or `Rye` (recommended for dependency management and virtual environments)

## Development Workflow and GitHub Repository Structure

1.  **Initialize GitHub Repository**:
    * Create a new GitHub repository (e.g., `PyDichroViz`).
    * Add a `.gitignore` file (to ignore `.pyc`, `__pycache__/`, `venv/`, `.DS_Store`, etc.).
    * Choose an appropriate open-source license (e.g., MIT License).
    * Create a `README.md` file, including a project overview, installation instructions, and quick usage examples.

2.  **Project Structure**:

    ```
    PyDichroViz/
    ├── .gitignore
    ├── LICENSE
    ├── pyproject.toml  (or requirements.txt)
    ├── README.md
    ├── src/
    │   └── pydichroviz/
    │       ├── __init__.py
    │       ├── crystallography.py
    │       ├── csl_calculator.py
    │       ├── dichromatic_plotter.py
    │       └── utils.py
    ├── examples/
    │   ├── basic_fcc_sigma3.ipynb  (Jupyter Notebook example)
    │   └── custom_bcc_plot.py      (Python script example)
    ├── tests/
    │   ├── test_crystallography.py
    │   ├── test_csl_calculator.py
    │   └── test_utils.py
    └── docs/  (Optional, for generating professional documentation)
        └── ...
    ```

3.  **Phased Implementation**:
    * **Phase 1: Basic Crystallography and Atom Generation**
        * Implement unit cell generation and coordinate transformation functions in `utils.py`.
        * Implement the `Crystal` class in `crystallography.py`, ensuring correct supercell atom point generation.
    * **Phase 2: CSL Calculation**
        * Implement rotation matrix conversion functions in `utils.py`.
        * Implement the `CSLCalculator` in `csl_calculator.py`, especially the `find_coincidence_points` method, which is critical for performance.
    * **Phase 3: 2D Plotting**
        * Implement the `plot_2d` method in `dichromatic_plotter.py`.
        * Create the first basic example in `examples/`.
    * **Phase 4: 3D Plotting and** $\Sigma$ **Value Calculation**
        * Implement the `plot_3d` method in `dichromatic_plotter.py`.
        * Implement the `calculate_sigma_value` method in `csl_calculator.py`.
    * **Phase 5: Testing and Optimization**
        * Write comprehensive `pytest` unit tests.
        * Perform performance analysis and optimization, especially for `find_coincidence_points`.
        * Refine documentation and examples.

## Advanced Features (Roadmap)

After implementing the core functionalities, consider adding the following advanced features:

* **Interactive GUI**: Quickly build a simple web interface using `Streamlit` or `Dash` to allow users to generate dichromatic plots without writing code.
* **File Import/Export**: Support importing crystal structures from common formats (e.g., POSCAR, CIF).
* **Grain Boundary Plane Specification**: Allow users to specify the grain boundary plane normal and visualize atoms near this plane.
* **Brandon Criterion Integration**: Integrate the Brandon criterion for tolerance in $\Sigma$ value calculations.
* **Grain Boundary Dislocation Visualization**: Identify and visualize grain boundary dislocations (DSC lattice).
* **Performance Optimization**: Explore more advanced parallel computing or GPU acceleration for very large supercells or complex structures.
* **Richer Plotting Options**: For example, adding crystallographic direction markers, plane markers, crystal boundary lines, etc.

## Important Considerations

* **Floating-Point Precision**: When comparing atom positions for coincidence, due to floating-point calculation limitations, a reasonable tolerance value must be used instead of strict equality.
* **Performance**: The quadratic increase in atom count can quickly impact calculation performance. `KDTree` is key to addressing efficiency issues in nearest-neighbor search.
* **Coordinate System Consistency**: Ensure a consistent coordinate system is used throughout the library (e.g., always use Cartesian coordinates for calculations, or perform explicit Cartesian-to-fractional conversions when necessary).
* **Documentation and Examples**: Clear documentation and rich examples are crucial for the success of an open-source project.
* **Testing**: Write comprehensive test cases to ensure the correctness and robustness of the code.

This project has great potential. Good luck with your development!
