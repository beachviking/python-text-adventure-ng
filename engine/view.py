from abc import ABC, abstractmethod
from .command import Command
from colorama import init, Fore, Style


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

    def get_raw_command(self) -> str:
        """Displays a simple prompt and gets a raw string command."""
        try:
            return input("\n> ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"


class ColoramaView(View):
    """
    A fun and whimsical command-line view that uses colorama and emojis for styling.
    """

    def __init__(self):
        init(autoreset=True)
        # The color palette remains the same
        self.LOCATION_STYLE = Fore.CYAN + Style.BRIGHT
        self.EXITS_STYLE = Fore.GREEN
        self.ITEMS_STYLE = Fore.YELLOW
        self.PROMPT_STYLE = Fore.MAGENTA + Style.BRIGHT
        self.MESSAGE_STYLE = Fore.WHITE
        self.ERROR_STYLE = Fore.RED + Style.BRIGHT
        self.SEPARATOR_STYLE = Fore.BLUE + Style.DIM

    def render_scene(self, scene_description: str, exits: list[str], items: list[str]):
        separator = self.SEPARATOR_STYLE + "~" * 50
        print(f"\n{separator}")
        # NEW: Added a compass emoji
        print(self.LOCATION_STYLE + f"🧭 {scene_description}")
        if items:
            # NEW: Added a magnifying glass emoji
            print(self.ITEMS_STYLE + f"🔎 You see: {', '.join(items)}")
        if exits:
            # NEW: Added a door emoji
            print(self.EXITS_STYLE + f"🚪 Obvious exits are: {', '.join(exits)}")
        print(separator)

    def render_player_state(self, inventory: list[str], attributes: str):
        if inventory:
            # NEW: Added a backpack emoji
            print(Style.BRIGHT + f"🎒 You are carrying: {', '.join(inventory)}")
        # NEW: Added a scroll emoji
        print(f"📜 Attributes: {attributes}")

    def render_message(self, message: str):
        if message:
            # NEW: Added a speech bubble emoji
            print(self.MESSAGE_STYLE + f"💬 {message}")

    def get_raw_command(self) -> str:
        """The CLI-specific input prompt (already whimsical!)."""
        try:
            return input(self.PROMPT_STYLE + "✨ > ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"

    def get_menu_choice(self, choices: list[Command]) -> Command:
        """The Menu-specific input prompt, now with more magic."""
        # NEW: Added a magic wand emoji
        print(self.PROMPT_STYLE + "\n--- 🪄 What wondrous deed to do? ---")
        for i, command in enumerate(choices, 1):
            print(f"{self.LOCATION_STYLE}{i}. {Style.RESET_ALL}{command.description}")
        print(self.PROMPT_STYLE + "----------------------------------")

        while True:
            # NEW: Added a crystal ball emoji
            choice = input(self.PROMPT_STYLE + "Choose thy fate 🔮: ")
            if choice.isdigit() and 1 <= int(choice) <= len(choices):
                return choices[int(choice) - 1]
            self.render_message(
                self.ERROR_STYLE + "A most invalid choice! Pray, try again."
            )


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

    def get_menu_choice(self, choices: list[Command]) -> Command:
        """Displays a menu of commands and gets the user's choice."""
        print("\n--- Choices ---")
        for i, command in enumerate(choices, 1):
            print(f"{i}. {command.description}")
        print("---------------")

        while True:
            choice = input("What do you do? ")
            if choice.isdigit() and 1 <= int(choice) <= len(choices):
                return choices[int(choice) - 1]
            self.render_message("Invalid choice. Please enter a number from the list.")
