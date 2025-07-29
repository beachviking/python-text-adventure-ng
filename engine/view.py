from abc import ABC, abstractmethod
from .command import Command

class View(ABC):
    """The base interface for all game views."""

    @abstractmethod
    def render_scene(self, scene_description: str, exits: list[str], items: list[str]):
        """Renders the primary description of a location."""
        pass

    @abstractmethod
    def render_player_state(self, inventory: list[str], attributes: str):
        """Renders the player's status."""
        pass

    @abstractmethod
    def render_message(self, message: str):
        """Renders a feedback message from a command or event."""
        pass

class CliView(View):
    """A view for a classic command-line interface."""
    
    # --- The render methods are the same as before ---
    def render_scene(self, scene_description: str, exits: list[str], items: list[str]):
        print("\n" + "#" * 40)
        print(scene_description)
        if items:
            print(f"You see: {', '.join(items)}")
        if exits:
            print(f"Obvious exits are: {', '.join(exits)}")
        print("#" * 40)

    def render_player_state(self, inventory: list[str], attributes: str):
        if inventory:
            print(f"You are carrying: {', '.join(inventory)}")
        print(f"Attributes: {attributes}")

    def render_message(self, message: str):
        if message:
            print(message)

    # --- THIS METHOD IS UNIQUE TO THE CLI VIEW ---
    def get_raw_command(self) -> str:
        """Displays a simple prompt and gets a raw string command."""
        try:
            return input('\n> ').lower().strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"
        
class MenuView(View):
    """A view for a classic menu-driven interface."""

    def render_scene(self, scene_description: str, exits: list[str], items: list[str]):
        print("\n" + "#" * 40)
        print(scene_description)
        if items:
            print(f"You see: {', '.join(items)}")
        if exits:
            print(f"Obvious exits are: {', '.join(exits)}")
        print("#" * 40)

    def render_player_state(self, inventory: list[str], attributes: str):
        if inventory:
            print(f"You are carrying: {', '.join(inventory)}")
        print(f"Attributes: {attributes}")

    def render_message(self, message: str):
        if message:
            print(message)

    # --- THIS METHOD IS UNIQUE TO THE MENU VIEW ---
    def get_menu_choice(self, choices: list[Command]) -> Command:
        """Displays a menu of commands and gets the user's choice."""
        print("\n--- Choices ---")
        for i, command in enumerate(choices, 1):
            print(f'{i}. {command.description}')
        print("---------------")
        
        while True:
            choice = input('What do you do? ')
            if choice.isdigit() and 1 <= int(choice) <= len(choices):
                return choices[int(choice) - 1]
            self.render_message('Invalid choice. Please enter a number from the list.')
