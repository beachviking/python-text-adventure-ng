from typing import Callable
from .inventory_item import InventoryItem
# NOTE: We DO NOT import Place at the top level to avoid circular dependencies.

class Transition:
    """
    Represents a one-way path from one Place to another,
    which may have conditions or require a key.
    """
    place: 'Place'
    condition: Callable[[], bool] | None
    key: InventoryItem | None

    def __init__(self, place: 'Place', condition: Callable[[], bool] | None = None, key: InventoryItem | None = None, direction: str | None = None):
        # This local import is the key to breaking the circular dependency.
        from .place import Place
        assert isinstance(place, Place)

        self.place = place
        self.condition = condition
        self.key = key
        self.direction = direction


    def is_accessible(self, game: 'Game') -> bool:
        """Checks if the player can use this transition."""
        if self.condition and not self.condition():
            return False
        # Check if the required key is in the game's inventory list
        if self.key and self.key not in game.inventory:
            return False
        return True    