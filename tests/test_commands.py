# In tests/test_commands.py

# We need to import the classes we want to test
from engine.game import Game
from engine.place import Place
from engine.inventory_item import InventoryItem
from engine.player_attributes import PlayerAttributes
from engine.command import TakeCommand, DropCommand, GoCommand
from engine.transition import Transition

# We also need a "mock" or "dummy" view and strategy for the Game object
from engine.view import View 
from engine.strategies import InputStrategy

# --- Create Dummy Classes for Testing ---
# We need these so we can create a Game instance without worrying about real I/O.
class MockView(View):
    def render_scene(self, *args, **kwargs): pass
    def render_player_state(self, *args, **kwargs): pass
    def render_message(self, *args, **kwargs): pass

class MockStrategy(InputStrategy):
    def get_action(self, *args, **kwargs): pass

# --- The Test Class ---
# A test class groups related tests together.
class TestCommands:

    def setup_method(self):
        """
        pytest calls this method before running EACH test.
        This gives us a clean, predictable game state for every test.
        """
        # ARRANGE: Create a consistent "test world"
        self.game = Game("Health", MockStrategy(), MockView())
        self.game.attributes = PlayerAttributes({'Health': 100})
        
        self.key = InventoryItem("key", "A rusty old key.")
        self.sword = InventoryItem("sword", "A sharp, shiny sword.")

        self.start_room = Place("Start Room", "A simple room.", inventory_items=[self.key])
        self.end_room = Place("End Room", "A different room.")
        
        self.game.location = self.start_room
        self.game.inventory = [self.sword] # Player starts with a sword

    def test_take_command_executes_correctly(self):
        """
        Tests if the TakeCommand moves an item from the room to the player's inventory.
        """
        # ARRANGE: The `setup_method` has already created the world. We just need the command.
        command = TakeCommand(self.key)

        # ACT: Execute the command on our test game state.
        result = command.execute(self.game)

        # ASSERT: Check if the world changed in the way we expected.
        assert self.key not in self.start_room.inventory_items # Key should be gone from room
        assert self.key in self.game.inventory # Key should be in player's inventory
        assert result.message == "You take the key." # The result message should be correct

    def test_drop_command_executes_correctly(self):
        """
        Tests if the DropCommand moves an item from the player to the room.
        """
        # ARRANGE: The player starts with a sword. Create the command to drop it.
        command = DropCommand(self.sword)

        # ACT: Execute the command.
        result = command.execute(self.game)

        # ASSERT: Check the results.
        assert self.sword in self.start_room.inventory_items # Sword should now be in the room
        assert self.sword not in self.game.inventory # Sword should be gone from player
        assert result.message == "You drop the sword."

    def test_go_command_fails_if_locked(self):
        """
        Tests if a transition requiring a key is inaccessible without that key.
        """
        # ARRANGE: Create a locked transition. The player does NOT have the 'gem' key.
        gem = InventoryItem("gem", "A glowing gem.")
        locked_transition = Transition(self.end_room, key=gem)
        command = GoCommand(locked_transition)

        # ACT: Attempt to execute the command.
        result = command.execute(self.game)

        # ASSERT: Check that nothing changed.
        assert self.game.location == self.start_room # Player should NOT have moved
        assert result.message == "You can't go that way right now." # Check for failure message

    def test_go_command_succeeds_if_unlocked(self):
        """
        Tests if a transition requiring a key IS accessible if the player has the key.
        """
        # ARRANGE
        # 1. Create the locked transition.
        gem = InventoryItem("gem", "A glowing gem.")
        locked_transition = Transition(self.end_room, key=gem)
        command = GoCommand(locked_transition)

        # 2. CRITICAL STEP: Put the key in the player's inventory *before* the action.
        self.game.inventory.append(gem)

        # ACT: Execute the command.
        result = command.execute(self.game)

        # ASSERT
        # 1. Check that the player successfully moved to the new room.
        assert self.game.location == self.end_room
        
        # 2. Check that the command result indicates a location change.
        assert result.location_changed is True
        assert result.message == "" # Successful moves have an empty message        