# In engine/command.py

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# NEW: Import the result object
from .command_result import CommandResult

if TYPE_CHECKING:
    from .game import Game
    from .transition import Transition
    from .inventory_item import InventoryItem
    from .activity import Activity


class Command(ABC):
    def __init__(self, description: str | None = None):
        self.description = description

    @abstractmethod
    def execute(self, game: Game) -> CommandResult:  # Return type is now CommandResult
        pass


class GoCommand(Command):
    def __init__(self, transition: Transition):
        self.transition = transition
        # We can also give non-selectable commands a description for debugging
        super().__init__(description=f"Go to {transition.place.name}")

    def execute(self, game: Game) -> CommandResult:
        if self.transition.is_accessible(game):
            game.location = self.transition.place
            # Return a result with the location_changed flag set to True
            return CommandResult(message="", location_changed=True)
        else:
            return CommandResult(message="You can't go that way right now.")


class TakeCommand(Command):
    def __init__(self, item: InventoryItem):
        self.item = item
        super().__init__(description=f"Take {item.name}")

    def execute(self, game: Game) -> CommandResult:
        game.location.inventory_items.remove(self.item)
        game.inventory.append(self.item)
        return CommandResult(message=f"You take the {self.item.name}.")


class DropCommand(Command):
    def __init__(self, item: InventoryItem):
        self.item = item
        super().__init__(description=f"Drop {item.name}")

    def execute(self, game: Game) -> CommandResult:
        game.inventory.remove(self.item)
        game.location.inventory_items.append(self.item)
        return CommandResult(message=f"You drop the {self.item.name}.")


class InventoryCommand(Command):
    def __init__(self):
        super().__init__(description="Check inventory")

    def execute(self, game: Game) -> CommandResult:
        if not game.inventory:
            return CommandResult(message="You aren't carrying anything.")
        else:
            inventory_names = [item.name for item in game.inventory]
            return CommandResult(
                message=f"You are carrying: {', '.join(inventory_names)}"
            )


class LookCommand(Command):
    """A command to look at the room or a specific item."""

    def __init__(self, target: str | None = None):
        self.target = target
        # Set the description based on whether there's a target
        description = "Look around" if not target else f"Look at {target}"
        super().__init__(description=description)

    def execute(self, game: Game) -> CommandResult:
        # Case 1: Simple "look" command
        if not self.target:
            # Trigger a full scene re-render by setting location_changed = True
            return CommandResult(message="", location_changed=True)

        # Case 2: "look <target>" command
        # Search for the target item in the room and in the player's inventory
        search_areas = game.location.inventory_items + game.inventory
        for item in search_areas:
            if self.target.lower() in item.name.lower():
                # Found the item! Return its detailed description.
                return CommandResult(message=item.description)

        # If we get here, the item wasn't found
        return CommandResult(message=f"You don't see a '{self.target}' here.")


class HelpCommand(Command):
    def __init__(self):
        super().__init__(description="Show help")

    def execute(self, game: Game) -> CommandResult:
        # The strategy now has the verb_map, so we pass it to the command
        # This requires a small change to the Game class __init__
        # to pass the strategy to the HelpCommand.
        # A simpler way for now: hardcode the help text.

        help_text = (
            "Available commands:\n"
            "  - go [direction/place]\n"
            "  - look / look [item]\n"
            "  - take [item]\n"
            "  - drop [item]\n"
            "  - inventory (or i)\n"
            "  - help\n"
            "  - quit"
        )
        return CommandResult(message=help_text)


class QuitCommand(Command):
    def __init__(self):
        super().__init__(description="Quit game")

    def execute(self, game: Game) -> CommandResult:
        # Set the game_over flag to True
        return CommandResult(message="Goodbye!", game_over=True)
