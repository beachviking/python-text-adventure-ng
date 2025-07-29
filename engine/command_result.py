from dataclasses import dataclass

@dataclass
class CommandResult:
    """An object to hold the results of an executed command."""
    message: str
    location_changed: bool = False
    game_over: bool = False