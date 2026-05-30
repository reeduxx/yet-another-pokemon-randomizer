from dataclasses import dataclass
from src.games.base import GameDefinition, ROMMetadata
from src.games.registry import GameRegistry


@dataclass(slots=True)
class DummyGameDefinition(GameDefinition):
    expected_title: str = "POKEMON BLUE"

    def get_species_ids(self) -> tuple[int, ...]:
        return (1, 2, 3)

    def matches(self, metadata: ROMMetadata) -> bool:
        return metadata.title == self.expected_title


class DummyLoader:
    def load_directory(self, directory):
        return [{"name": "dummy"}]


class DummyFactory:
    def create(self, definition):
        return DummyGameDefinition(
            name="POKéMON BLUE",
            internal_title="POKEMON BLUE",
            generation=1,
        )


def test_load_definitions_loads_games_from_directory():
    registry = GameRegistry()
    registry.loader = DummyLoader()
    registry.factory = DummyFactory()
    registry.load_definitions("fake/path")

    assert len(registry.games) == 1
    assert registry.games[0].name == "POKéMON BLUE"


def test_detect_game_returns_matching_game():
    registry = GameRegistry()
    game = DummyGameDefinition(
        name="POKéMON BLUE",
        internal_title="POKEMON BLUE",
        generation=1,
    )
    registry.games = [game]
    metadata = ROMMetadata(size=1024, title="POKEMON BLUE")
    detected = registry.detect_game(metadata)

    assert detected is game


def test_detect_game_returns_none_when_no_game_matches():
    registry = GameRegistry()
    game = DummyGameDefinition(
        name="POKéMON BLUE",
        internal_title="POKEMON BLUE",
        generation=1,
    )
    registry.games = [game]
    metadata = ROMMetadata(size=1024, title="POKEMON RED")
    detected = registry.detect_game(metadata)

    assert detected is None


def test_load_definitions_includes_existing_user_directory(tmp_path):
    app_directory = tmp_path / "data"
    user_directory = tmp_path / "user_data"
    app_directory.mkdir()
    user_directory.mkdir()

    class DummyLoaderWithDirectories:
        def load_directory(self, directory):
            if directory == app_directory:
                return [{"name": "data"}]
            if directory == user_directory:
                return [{"name": "user_data"}]
            return []

    class DummyFactoryWithNames:
        def create(self, definition):
            return DummyGameDefinition(
                name=definition["name"],
                internal_title=definition["name"].upper(),
                generation=1,
            )

    registry = GameRegistry()
    registry.loader = DummyLoaderWithDirectories()
    registry.factory = DummyFactoryWithNames()
    registry.load_definitions(app_directory, user_directory)

    assert [game.name for game in registry.games] == ["data", "user_data"]


def test_load_definitions_ignores_missing_user_directory(tmp_path):
    app_directory = tmp_path / "data"
    missing_user_directory = tmp_path / "user_data"
    app_directory.mkdir()
    registry = GameRegistry()
    registry.loader = DummyLoader()
    registry.factory = DummyFactory()
    registry.load_definitions(app_directory, missing_user_directory)

    assert len(registry.games) == 1
