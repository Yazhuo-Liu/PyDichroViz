import json
import math
from pathlib import Path
from typing import Dict, Any, Union
from jsonschema import validate, ValidationError
from .schema import CRYSTAL_DATA_SCHEMA

class CrystalDataParser:
    def __init__(self):
        """
        Initialize the parser with default mathematical constants.
        These can be overridden or extended by the JSON input file.
        """
        self.constants = {
            "sqrt2": math.sqrt(2),
            "sqrt2_div_2": math.sqrt(2) / 2,
            "sqrt2_div_4": math.sqrt(2) / 4
        }

    def parse_value(self, value: Any) -> Union[float, str]:
        """
        Parse a single value. If it's a string starting with '@',
        replace it with the corresponding constant.

        Args:
            value (Any): The value to parse.

        Returns:
            Union[float, str]: Parsed float or original value if not an expression.

        Raises:
            KeyError: If an undefined constant is referenced.
        """
        if isinstance(value, str) and value.startswith("@"):
            key = value[1:]
            if key not in self.constants:
                raise KeyError(f"Undefined constant '{key}' used in JSON data.")
            return self.constants[key]
        return value

    def resolve_expressions(self, data: Any) -> Any:
        """
        Recursively resolve expressions in nested data structures.

        Args:
            data (Any): The input data structure (dict/list/value).

        Returns:
            Any: The resolved data structure with all expressions replaced.
        """
        if isinstance(data, dict):
            return {k: self.resolve_expressions(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve_expressions(item) for item in data]
        else:
            return self.parse_value(data)

    def load_and_parse(self, file_path: Path) -> Dict[str, Any]:
        """
        Load, validate and parse crystal structure data from a JSON file.

        Args:
            file_path (Path): Path to the JSON file containing crystal data.

        Returns:
            Dict[str, Any]: Parsed data dictionary with all expressions resolved.
        """
        try:
            # Step 1: Load raw JSON
            with open(file_path, 'r') as f:
                raw_data = json.load(f)

            # Step 2: Validate schema
            try:
                validate(instance=raw_data, schema=CRYSTAL_DATA_SCHEMA)
            except ValidationError as ve:
                raise ValueError(f"Schema validation failed: {ve.message}") from ve

            # Validate _expressions type if present
            if "_expressions" in raw_data:
                if not isinstance(raw_data["_expressions"], dict):
                    raise ValueError(
                        "'_expressions' field must be a dictionary (object), "
                        f"but got {type(raw_data['_expressions']).__name__}."
                    )
            
            # Step 3: Merge user-defined expressions
            if "_expressions" in raw_data:
                self.constants.update(raw_data["_expressions"])

            # Step 4: Resolve all expressions recursively
            resolved_data = self.resolve_expressions(raw_data)

            # Step 5: Promote periods to top-level fields
            if "periods" in resolved_data:
                resolved_data.update({
                    "x_period": resolved_data["periods"]["x"],
                    "y_period": resolved_data["periods"]["y"],
                    "z_period": resolved_data["periods"]["z"]
                })

            return resolved_data

        except FileNotFoundError:
            raise FileNotFoundError(f"Crystal data file not found at path: {file_path}")
        except json.JSONDecodeError as je:
            raise ValueError(f"Invalid JSON format in file: {je}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while loading crystal data: {e}")


# ========================
# Example Usage
# ========================

if __name__ == "__main__":
    parser = CrystalDataParser()
    try:
        data = parser.load_and_parse(Path("crystal_data/fcc/110.json"))

        print("JSON data is valid and parsed successfully.\n")

        print("Meta Information:")
        print(f"Crystal System: {data['_meta']['crystal_system']}")
        print(f"Plane: {data['_meta']['plane']}")

        print("\nAtomic Positions:")
        for pos in data["basis"]["positions"]:
            print(f"- {pos}")

        print("\nResolved Values:")
        print(f"X Period: {data['x_period']} (≈√2)")
        print(f"Y Period: {data['y_period']} (≈1.0)")
        print(f"Z Period: {data['z_period']} (≈√2/2)")
        print(f"Z Layer Offset: {data['out_of_plane_offsets'][1]} (≈√2/4)")

    except Exception as e:
        print(f"[ERROR] Failed to process crystal data: {e}")