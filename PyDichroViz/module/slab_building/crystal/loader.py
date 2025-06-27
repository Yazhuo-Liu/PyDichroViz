from pathlib import Path
from parser import CrystalDataParser

class CrystalStructureLoader:
    def __init__(self, crystal_system: str, plane: str, base_dir: Path = None):
        """
        Initialize the loader with crystal system and plane.

        Args:
            crystal_system (str): e.g., 'fcc', 'bcc', 'sc'
            plane (str): e.g., '100', '110', '111'
            base_dir (Path): Directory containing subfolders of crystal systems.
                             If not provided, defaults to 'data/structures/'
        """
        self.crystal_system = crystal_system.lower()
        self.plane = plane
        self.base_dir = base_dir or Path(__file__).parent.parent / "crystal_data"

    def find_structure_file(self) -> Path:
        """
        Search for a matching JSON file based on crystal system and plane.

        Returns:
            Path: Path to the matching JSON file.

        Raises:
            FileNotFoundError: If no matching file is found.
        """
        crystal_dir = self.base_dir / self.crystal_system
        candidate = crystal_dir / f"{self.plane}.json"

        if not candidate.exists():
            raise FileNotFoundError(
                f"No structure file found for {self.crystal_system}({self.plane}) "
                f"at expected path: {candidate}"
            )

        return candidate

    def load_structure(self) -> dict:
        """
        Load and validate the crystal structure data.

        Returns:
            dict: Parsed crystal structure data.

        Raises:
            ValueError: If metadata mismatch detected.
        """
        parser = CrystalDataParser()
        json_path = self.find_structure_file()
        data = parser.load_and_parse(json_path)

        # Validate meta consistency
        meta = data["_meta"]
        if (
            meta["crystal_system"].lower() != self.crystal_system
            or meta["plane"] != self.plane
        ):
            raise ValueError(
                f"Metadata mismatch in {json_path}: "
                f"Expected {self.crystal_system}({self.plane}), "
                f"found {meta['crystal_system']}({meta['plane']})"
            )

        return data


# ================================================
# Test Cases (Main Guard)
# ================================================

if __name__ == "__main__":
    import pprint

    pp = pprint.PrettyPrinter(indent=2)

    test_cases = [
        {"crystal_system": "fcc", "plane": "110"},
        {"crystal_system": "bcc", "plane": "100"},
    ]

    for case in test_cases:
        print(f"\nTesting: {case['crystal_system']}({case['plane']})")
        try:
            loader = CrystalStructureLoader(**case)
            data = loader.load_structure()
            print("Successfully loaded structure.")
            print("Meta Info:")
            pp.pprint(data["_meta"])
        except Exception as e:
            print(f"Error: {e}")