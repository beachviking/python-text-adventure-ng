# In a NEW file: tests/test_strategies.py

import pytest
from engine.game import Game
from engine.place import Place
from engine.inventory_item import InventoryItem
from engine.player_attributes import PlayerAttributes
from engine.transition import Transition

# We are testing the strategy, so we need to import it.
from engine.strategies import CliInputStrategy

# We are checking the command objects it returns.
from engine.command import TakeCommand, GoCommand, InventoryCommand

# We need a mock view that we can program with fake user input.
from engine.view import View

class ControllableMockView(View):
    """A mock view where we can set the next command the 'user' will type."""
    def __init__(self):
        self.command_to_return = ""

    def set_next_command(self, command: str):
        self.command_to_return = command
    
    # --- The required methods from the View interface ---
    def render_scene(self, *args, **kwargs): pass
    def render_player_state(self, *args, **kwargs): pass
    def render_message(self, *args, **kwargs): pass
    
    # --- This is the important one for our test ---
    def get_raw_command(self) -> str:
        # Instead of calling input(), it just returns the string we told it to.
        return self.command_to_return

# --- The Test Class ---
class TestCliInputStrategy:

    def setup_method(self):
        """Set up a consistent game world for each test."""
        # Create a controllable view and the strategy we want to test
        self.mock_view = ControllableMockView()
        self.strategy = CliInputStrategy()
        
        # We still need a Game object for the strategy to query
        # This one doesn't need a real strategy, so we can pass None.
        self.game = Game("Health", None, self.mock_view)
        self.game.attributes = PlayerAttributes({'Health': 100})
        
        self.key = InventoryItem("key", "A rusty key.")
        self.start_room = Place("Start Room", "A room.", inventory_items=[self.key])
        self.north_room = Place("North Room", "Another room.")
        
        # Create a directional transition for the 'go north' test
        self.start_room.add_transitions(Transition(self.north_room, direction='north'))
        
        self.game.location = self.start_room

    def test_parser_handles_simple_take_command(self):
        """
        Tests if typing "take key" returns a correct TakeCommand.
        """
        # ARRANGE: Tell our mock view that the next "typed" command will be "take key"
        self.mock_view.set_next_command("take key")

        # ACT: Run the strategy's get_action method.
        result_command = self.strategy.get_action(self.game, self.mock_view)

        # ASSERT
        # 1. Check that the returned object is the right type of command.
        assert isinstance(result_command, TakeCommand)
        
        # 2. Check that the command contains the correct item.
        assert result_command.item == self.key

    def test_parser_handles_directional_go_command(self):
        """
        Tests if typing "go north" returns a correct GoCommand.
        """
        # ARRANGE
        self.mock_view.set_next_command("go north")

        # ACT
        result_command = self.strategy.get_action(self.game, self.mock_view)

        # ASSERT
        assert isinstance(result_command, GoCommand)
        # Check that the command contains the transition that leads to the North Room.
        assert result_command.transition.place == self.north_room

    def test_parser_handles_simple_verb(self):
        """
        Tests if typing "i" returns a correct InventoryCommand.
        """
        # ARRANGE
        self.mock_view.set_next_command("i")

        # ACT
        result_command = self.strategy.get_action(self.game, self.mock_view)

        # ASSERT
        assert isinstance(result_command, InventoryCommand)