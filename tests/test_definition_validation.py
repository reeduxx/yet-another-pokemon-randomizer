import json
import pytest
from src.games.definitions.loader import DefinitionLoader, DefinitionLoaderError


def write_definition(path, data):
    """Write definition test data to a JSON file."""
    path.write_text(json.dumps(data), encoding="utf-8")


def valid_definition():
    """Return a minimal valid ROM definition."""
    return {
        "version": 1,
        "generation": 1,
        "metadata": {
            "name": "POKEMON BLUE",
            "internal_title": "POKEMON BLUE",
            "language_code": "E",
            "revision": "v1.0",
            "version_byte": "0x00",
            "header_checksum": "0xD3",
            "global_checksum": "0x9D0A",
        },
        "offsets": {
            "species_name_table": "0x1C21E",
        },
    }


def test_definition_requires_version(tmp_path):
    data = valid_definition()
    data.pop("version")
    definition_path = tmp_path / "missing_version.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_requires_generation(tmp_path):
    data = valid_definition()
    data.pop("generation")
    definition_path = tmp_path / "missing_generation.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_requires_metadata(tmp_path):
    data = valid_definition()
    data.pop("metadata")
    definition_path = tmp_path / "missing_metadata.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_requires_offsets(tmp_path):
    data = valid_definition()
    data.pop("offsets")
    definition_path = tmp_path / "missing_offsets.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_rejects_unsupported_version(tmp_path):
    data = valid_definition()
    data["version"] = 999
    definition_path = tmp_path / "unsupported_version.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_rejects_invalid_hex_metadata_value(tmp_path):
    data = valid_definition()
    data["metadata"]["header_checksum"] = "0xGG"
    definition_path = tmp_path / "invalid_hex_metadata.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_rejects_unknown_metadata_field(tmp_path):
    data = valid_definition()
    data["metadata"]["unexpected_field"] = "0x00"
    definition_path = tmp_path / "unknown_metadata_field.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_rejects_invalid_hex_offset_value(tmp_path):
    data = valid_definition()
    data["offsets"]["species_name_table"] = "0xGG"
    definition_path = tmp_path / "invalid_hex_offset.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_rejects_invalid_offset_type(tmp_path):
    data = valid_definition()
    data["offsets"]["species_name_table"] = {"bad": "type"}
    definition_path = tmp_path / "invalid_offset_type.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_rejects_non_object_metadata(tmp_path):
    data = valid_definition()
    data["metadata"] = ["not", "an", "object"]
    definition_path = tmp_path / "non_object_metadata.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)


def test_definition_rejects_non_object_offsets(tmp_path):
    data = valid_definition()
    data["offsets"] = ["not", "an", "object"]
    definition_path = tmp_path / "non_object_offsets.json"
    write_definition(definition_path, data)
    loader = DefinitionLoader()

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(definition_path)
