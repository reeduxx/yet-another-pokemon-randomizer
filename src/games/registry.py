from games.base import ROMMetadata
from games.gen1.blue import BLUE_VERSIONS
from games.gen1.green import GREEN_VERSIONS
from games.gen1.red import RED_VERSIONS
from games.gen1.yellow import YELLOW_VERSIONS

SUPPORTED_GAMES = [
    *RED_VERSIONS,
    *GREEN_VERSIONS,
    *BLUE_VERSIONS,
    *YELLOW_VERSIONS,
]

def detect_game(rom) -> object | None:
    metadata = rom.get_metadata()
    
    for game in SUPPORTED_GAMES:
        if game.matches(metadata):
            return game
    
    return None