# ========================
# Schema Definition for Crystal Structure Files
# ========================

CRYSTAL_DATA_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema ",
    "title": "Crystal Structure Data Schema",
    "type": "object",
    "required": ["_meta", "basis", "layers_per_supercell", "in_plane_offsets", "out_of_plane_offsets", "periods"],
    "properties": {
        "_meta": {
            "type": "object",
            "required": ["crystal_system", "plane", "description", "source"],
            "properties": {
                "crystal_system": {"type": "string", "enum": ["fcc", "bcc", "sc", "hcp"]},
                "plane": {"type": "string", "pattern": "^\\d{3}$"},
                "description": {"type": "string"},
                "source": {"type": "string"}
            }
        },
        "_units": {
            "type": "object",
            "required": ["positions", "offsets", "periods"],
            "properties": {
                "positions": {"type": "string"},
                "offsets": {"type": "string"},
                "periods": {"type": "string"}
            }
        },
        "_expressions": {
            "type": "object",
            "additionalProperties": {"type": "number"},
            "description": "Custom-defined mathematical expressions"
        },
        "basis": {
            "type": "object",
            "required": ["positions"],
            "properties": {
                "positions": {
                    "type": "array",
                    "items": {
                        "type": ["array", "number", "string"],
                        "minItems": 2,
                        "maxItems": 2,
                        "items": {"type": ["number", "string"]}
                    }
                },
                "comment": {"type": "string"}
            }
        },
        "layers_per_supercell": {"type": "integer", "minimum": 1},
        "in_plane_offsets": {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": {"type": ["number", "string"]}
            }
        },
        "out_of_plane_offsets": {
            "type": "array",
            "items": {"type": ["number", "string"]}
        },
        "periods": {
            "type": "object",
            "required": ["x", "y", "z"],
            "properties": {
                "x": {"type": ["number", "string"]},
                "y": {"type": ["number", "string"]},
                "z": {"type": ["number", "string"]}
            }
        }
    },
    "additionalProperties": False
}