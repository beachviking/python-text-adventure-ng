# In engine/game.py

from time import sleep

from .event import Event
from .player_attributes import PlayerAttributes
from .strategies import InputStrategy
from .view import View # <-- NEW: Import the View
from .command import Command # <-- NEW: Import the base Command
from .command_result import CommandResult # <-- NEW: Import the CommandResult

class Game:
    def __init__(self, attribute_name_for_suspense: str, input_strategy: InputStrategy, view: View):
        # Store the view and input strategy
        self.view = view
        self.input_strategy = input_strategy

        # Model Data
        self.location = None # Will be set by the subclass
        self.attributes = None # Will be set by the subclass
        self.inventory = []
        self._attribute_name_for_suspense = attribute_name_for_suspense
        Event.default_attribute = attribute_name_for_suspense
        self.is_running = True

    def _render_full_scene(self):
        """A helper method to render the complete game state via the View."""
        # 1. Prepare scene data from the model
        place = self.location
        exit_details = []
        for t in place.get_transitions():
            detail = t.place.name
            if t.direction:
                detail += f" ({t.direction})"
            exit_details.append(detail)
        
        item_names = [item.name for item in place.inventory_items]
        inventory_names = [item.name for item in self.inventory]

        # 2. Call the view methods to render
        self.view.render_scene(place.description, exit_details, item_names)
        self.view.render_player_state(inventory_names, str(self.attributes))

    def play(self):
        # Initial rendering of the first location
        self._render_full_scene()

        # The Presenter Loop
        while self.is_running:
            # Automatic events process the model directly
            self.location.process_events(self.attributes)

            # Check for game over from automatic events
            if self.attributes.attribs[self._attribute_name_for_suspense] <= 0:
                self.view.render_message(f"Your {self._attribute_name_for_suspense} is at 0. You lose.")
                self.is_running = False
                continue

            # 1. Get a command object from the input strategy
            command = self.input_strategy.get_action(self, self.view)
            
            if command:
                # 2. Execute the command on the model, get a result
                result = command.execute(self)

                # 3. Use the result to update the view and presenter state
                if result.game_over:
                    self.is_running = False
                
                # If location changed, re-render the entire scene
                if result.location_changed:
                    self._render_full_scene()
                
                # Always render the command's feedback message
                self.view.render_message(result.message)
