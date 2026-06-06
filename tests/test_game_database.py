from src.games.definitions.database.connection import create_connection
from src.games.definitions.database.importer import GameDefinitionImporter
from src.games.definitions.database.repository import GameDefinitionRepository
from src.games.definitions.database.schema import create_schema


def valid_definition():
    return {
        "version": 1,
        "generation": 1,
        "metadata": {
            "name": "POKEMON BLUE",
            "internal_title": "POKEMON BLUE",
            "language_code": "E",
            "revision": "v1.0",
            "version_byte": 0x00,
            "header_checksum": 0xD3,
            "global_checksum": 0x9D0A,
        },
        "offsets": {
            "species_name_table": 0x1C21E,
            "player_starter_offsets": [0x1D10E, 0x1D11F, 0x1D130],
            "optional_offset": None,
        },
    }


def test_create_schema_creates_game_definition_tables(tmp_path):
    database_path = tmp_path / "games.db"
    connection = create_connection(database_path)
    create_schema(connection)

    tables = {
        row["name"]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }

    assert "game_definitions" in tables
    assert "game_offsets" in tables


def test_repository_inserts_and_retrieves_definition(tmp_path):
    database_path = tmp_path / "games.db"
    connection = create_connection(database_path)
    create_schema(connection)
    repository = GameDefinitionRepository(connection)
    definition_id = repository.insert_definition(valid_definition())
    saved_definition = repository.get_definition(definition_id)

    assert saved_definition is not None
    assert saved_definition["generation"] == 1
    assert saved_definition["metadata"]["name"] == "POKEMON BLUE"
    assert saved_definition["offsets"]["species_name_table"] == 0x1C21E
    assert saved_definition["offsets"]["player_starter_offsets"] == [
        0x1D10E,
        0x1D11F,
        0x1D130,
    ]
    assert saved_definition["offsets"]["optional_offset"] is None


def test_repository_gets_all_definitions(tmp_path):
    database_path = tmp_path / "games.db"
    connection = create_connection(database_path)
    create_schema(connection)
    repository = GameDefinitionRepository(connection)
    first_id = repository.insert_definition(valid_definition())
    second_definition = valid_definition()
    second_definition["metadata"]["name"] = "POKEMON RED"
    second_id = repository.insert_definition(second_definition)
    definitions = repository.get_all_definitions()

    assert [definition["id"] for definition in definitions] == [first_id, second_id]
    assert definitions[0]["metadata"]["name"] == "POKEMON BLUE"
    assert definitions[1]["metadata"]["name"] == "POKEMON RED"


def test_importer_imports_multiple_definitions(tmp_path):
    database_path = tmp_path / "games.db"
    connection = create_connection(database_path)
    create_schema(connection)
    repository = GameDefinitionRepository(connection)
    importer = GameDefinitionImporter(repository)
    blue_definition = valid_definition()
    red_definition = valid_definition()
    red_definition["metadata"]["name"] = "POKEMON RED"
    imported_ids = importer.import_definitions([blue_definition, red_definition])
    definitions = repository.get_all_definitions()

    assert len(imported_ids) == 2
    assert len(definitions) == 2
    assert definitions[0]["metadata"]["name"] == "POKEMON BLUE"
    assert definitions[1]["metadata"]["name"] == "POKEMON RED"
