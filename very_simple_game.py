# 'A very simple example game using the text adventure engine.'
# CHANGED: This file is now updated to use the new, refactored engine.

from time import sleep

# CHANGED: All necessary imports from our new engine structure.
from engine.game import Game
from engine.place import Place
from engine.player_attributes import PlayerAttributes
from engine.transition import Transition
from engine.view import CliView, MenuView
from engine.strategies import MenuInputStrategy, CliInputStrategy


class VerySimple(Game):
    # CHANGED: The constructor now accepts the strategy and view from the launcher.
    def __init__(self, input_strategy, view):
        # CHANGED: Pass all required arguments to the parent Game class.
        # Even though this game doesn't use attributes, the engine needs a default.
        # We'll use 'Health' and just set it to a value that won't end the game.
        super().__init__('Health', input_strategy, view)
        
        # This will be set by the _define_world method.
        self.attributes = PlayerAttributes({'Health': 100})
        self.location = self._define_world()

    def _define_world(self) -> Place:
        """Creates and connects all the places in the game."""
        
        # Home
        home = Place('Home', 'You are at home.')

        # School
        school = Place('School', 'You are at school.')

        # Transitions
        # CHANGED: We now use directional transitions for a better CLI experience.
        # The new engine will automatically create a 'south' transition for the return trip.
        home.add_transitions(Transition(school, direction='north'), reverse=True)

        # Starting place
        return home


# NEW: The launcher block to select mode and start the game.
if __name__ == '__main__':
    # We define the introduction text here to be used by the launcher.
    introduction = 'Welcome to a Very Simple Game'

    mode = ""
    while mode not in ["1", "2"]:
        mode = input("Choose interaction mode:\n1. Menu\n2. CLI\nEnter 1 or 2: ")

    if mode == "1":
        strategy = MenuInputStrategy()
        view = MenuView()
    else: # mode == "2"
        strategy = CliInputStrategy()
        view = CliView()
    
    # Create the game instance with the chosen pair
    game = VerySimple(input_strategy=strategy, view=view)
    
    # The launcher is now responsible for displaying the introduction.
    view.render_message(introduction)
    sleep(1.5)
    
    game.play()