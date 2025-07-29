# 'An example game using the text adventure engine.'
# CHANGED: This file is now updated to use the new, refactored engine.

from time import sleep

from engine.command import Command, CommandResult
from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.player_attributes import PlayerAttributes
from engine.transition import Transition
from engine.view import CliView, MenuView
from engine.strategies import MenuInputStrategy, CliInputStrategy


# NEW: The custom action is now its own self-contained Command class.
class VisitFriendsCommand(Command):
    """A custom command for the "Visit with some friends" action."""
    def __init__(self):
        # The command provides its own description for the menu.
        super().__init__(description="Visit with some friends")

    def execute(self, game: 'ShipGame') -> CommandResult:
        # The logic is moved here. It now modifies the game state directly.
        game.friend_visits += 1
        
        # We can use a simpler check now. Let's say friends get tired after 3 visits.
        if game.friend_visits > 3:
            message = 'Your friends are tired of you. They make excuses and leave.'
            health_change = -5
        else:
            message = 'You visit with friends and have a few laughs.'
            health_change = 10
            
        # Modify the player's health attribute directly.
        game.attributes.attribs['Health'] += health_change
        
        # Return a result object instead of a number.
        return CommandResult(message=message)


class ShipGame(Game):
    # CHANGED: The constructor now accepts the strategy and view from the launcher.
    def __init__(self, input_strategy, view):
        # CHANGED: Pass all required arguments to the parent Game class.
        # The main attribute for this game is 'Health'.
        super().__init__('Health', input_strategy, view)
        
        # NEW: Custom game state is initialized here.
        self.friend_visits = 0
        
        # This will be set by the _define_world method.
        self.attributes = PlayerAttributes({'Health': 100})
        self.location = self._define_world()

    def _define_world(self) -> Place:
        """Creates and connects all the places in the game."""
        
        bridge = Place('Bridge',
            "You are on the bridge of a spaceship, sitting in the captain's chair.", [
                Event(0.01, 'Oh, no! An intruder beams onto the bridge and shoots you.', {'Health': -50}, max_occurrences=1),
                Event(0.1, "The ship's doctor gives you a health boost.", {'Health': 30}),
            ])

        ready_room = Place('Ready Room', "You are in the captain's ready room.", [
            Event(.5, 'The fish in the aquarium turn to watch you.', 0, max_occurrences=1),
        ])

        lift = Place('Lift', 'You have entered the turbolift.', [
            Event(.1, "The ship's android says hello to you.", {'Health': 1}),
        ])

        lounge = Place('Lounge', 'Welcome to the lounge.', [
            Event(1, 'Relaxing in the lounge improves your health.', {'Health': 10}),
        ])
        # CHANGED: We now add our new Command object to the lounge's event list.
        lounge.add_events(VisitFriendsCommand())

        # CHANGED: InventoryItem now requires a detailed description.
        space_suit = InventoryItem('Spacesuit', 'A standard-issue EVA suit, looks a bit bulky.')

        storage_room = Place('Storage Room', 'You enter the storage room',
            inventory_items=[space_suit])

        transporter_room = Place('Transporter Room',
            'The transporter room looks cool with all its blinking lights and sliders.')

        planet = Place('Planet', 'You have beamed down to the planet.', [
            Event(.3, 'You found the experience relaxing', {'Health': 10}),
        ])

        # CHANGED: Transitions are now directional for a better CLI experience.
        bridge.add_transitions(
            Transition(ready_room, direction='east'),
            Transition(lift, direction='west'),
            reverse=True
        )
        lift.add_transitions(
            Transition(lounge, direction='north'),
            Transition(storage_room, direction='south'),
            Transition(transporter_room, direction='west'),
            reverse=True
        )
        # CHANGED: The transition now uses the 'key=' keyword argument.
        transporter_room.add_transitions(Transition(planet, key=space_suit), reverse=True)

        return bridge


# NEW: The launcher block to select mode and start the game.
if __name__ == '__main__':
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
    game = ShipGame(input_strategy=strategy, view=view)
    
    view.render_message('Welcome to Ship Adventure. You are the captain of a star ship.')
    sleep(1.5)
    
    game.play()
