# crystal/loader.py

from pathlib import Path
import os
from typing import Dict, Any
from .parser import CrystalDataParser

class CrystalStructureLoader:
    def __init__(self, crystal_system: str, plane: str, structure_dir: Path = None):
        """
        Initialize the loader with crystal system and plane.

        Args:
            crystal_system (str): e.g., 'fcc', 'bcc', 'sc'
            plane (str): e.g., '100', '110', '111'
            structure_dir (Path): Directory containing crystal structure files.
                                  If not provided, defaults to `crystal/structures/`.
        """
        self.crystal_system = crystal_system.lower()
        self.plane = plane
        # 设置默认路径为当前模块下的 structures 目录
        self.structure_dir = structure_dir or self._get_default_structure_dir()

    def _get_default_structure_dir(self) -> Path:
        """Get the default structure directory inside the module."""
        module_dir = Path(os.path.dirname(__file__))  # 当前 loader.py 所在目录
        return module_dir / "structures"

    def find_structure_file(self) -> Path:
        """
        Search for a matching JSON file based on crystal system and plane.

        Returns:
            Path: Path to the matching JSON file.

        Raises:
            FileNotFoundError: If no matching file is found.
        """
        crystal_dir = self.structure_dir / self.crystal_system
        candidate = crystal_dir / f"{self.plane}.json"

        if not candidate.exists():
            raise FileNotFoundError(
                f"No structure file found for {self.crystal_system}({self.plane}) "
                f"at expected path: {candidate}"
            )

        return candidate

    def load_structure(self) -> Dict[str, Any]:
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
# 🔍 Test Cases (Main Guard)
# ================================================

if __name__ == "__main__":
    import pprint

    pp = pprint.PrettyPrinter(indent=2)

    test_cases = [
        {"crystal_system": "fcc", "plane": "110"},
        {"crystal_system": "bcc", "plane": "100"},
    ]

    for case in test_cases:
        print(f"\n🧪 Testing: {case['crystal_system']}({case['plane']})")
        try:
            loader = CrystalStructureLoader(**case)
            data = loader.load_structure()
            print("✅ Successfully loaded structure.")
            print("Meta Info:")
            pp.pprint(data["_meta"])
        except Exception as e:
            print(f"❌ Error: {e}")