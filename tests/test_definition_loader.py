import pytest
from src.games.definitions.loader import DefinitionLoader, DefinitionLoaderError


def test_load_file_raises_error_for_missing_file(tmp_path):
    loader = DefinitionLoader()
    missing_file = tmp_path / "missing.json"

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(missing_file)


def test_load_file_raises_error_for_invalid_json(tmp_path):
    loader = DefinitionLoader()
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{ invalid json", encoding="utf-8")

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(invalid_file)


def test_load_directory_raises_error_for_missing_directory(tmp_path):
    loader = DefinitionLoader()
    missing_directory = tmp_path / "missing_data"

    with pytest.raises(DefinitionLoaderError):
        loader.load_directory(missing_directory)


def test_load_directory_returns_empty_list_for_empty_directory(tmp_path):
    loader = DefinitionLoader()
    empty_directory = tmp_path / "empty_data"
    empty_directory.mkdir()
    definitions = loader.load_directory(empty_directory)

    assert definitions == []


def test_load_file_raises_error_for_invalid_definition_schema(tmp_path):
    loader = DefinitionLoader()
    invalid_file = tmp_path / "invalid_definition.json"
    invalid_file.write_text(
        """
        {
            "name": "POKéMON BLUE"
        }
        """,
        encoding="utf-8",
    )

    with pytest.raises(DefinitionLoaderError):
        loader.load_file(invalid_file)


def test_load_file_loads_valid_definition(tmp_path):
    loader = DefinitionLoader()
    definition_file = tmp_path / "pokemon_blue.json"
    definition_file.write_text(
        """
        {
            "version": 1, 
            "generation": 1, 
            "metadata": {
                "name": "POKéMON BLUE", 
                "internal_title": "POKEMON BLUE", 
                "language_code": "E", 
                "revision": "v1.0", 
                "version_byte": "0x00", 
                "header_checksum": "0xD3", 
                "global_checksum": "0x9D0A"
            },
            "offsets": {
                "species_name_table": "0x1C21E",
                "player_starter_offsets": ["0x1D10E", "0x1D11F", "0x1D130"]
            }
        }
        """,
        encoding="utf-8",
    )
    definition = loader.load_file(definition_file)

    assert definition["version"] == 1
    assert definition["generation"] == 1
    assert definition["metadata"]["name"] == "POKéMON BLUE"
    assert definition["metadata"]["version_byte"] == 0x00
    assert definition["metadata"]["header_checksum"] == 0xD3
    assert definition["metadata"]["global_checksum"] == 0x9D0A
    assert definition["offsets"]["species_name_table"] == 0x1C21E
    assert definition["offsets"]["player_starter_offsets"] == [
        0x1D10E,
        0x1D11F,
        0x1D130,
    ]
