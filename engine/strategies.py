from abc import ABC, abstractmethod

from .command import (
    Command,
    GoCommand,
    TakeCommand,
    DropCommand,
    InventoryCommand,
    QuitCommand,
    LookCommand,
    HelpCommand,
)

from .view import View, CliView, MenuView


class InputStrategy(ABC):
    @abstractmethod
    def get_action(self, game, view: View) -> Command | None:
        pass


class MenuInputStrategy(InputStrategy):
    """The Menu strategy, now updated to return Command objects."""

    def get_action(self, game, view: MenuView):
        # 1. Gather all possible commands from the current game state.
        location = game.location
        possible_commands = []

        # Add commands for transitions
        for t in location.get_transitions():
            possible_commands.append(GoCommand(t))

        # Add commands for selectable activities/events
        possible_commands.extend(location.get_selectable_commands())

        # Add commands for taking items
        for i in location.inventory_items:
            possible_commands.append(TakeCommand(i))

        # Add commands for dropping items
        for i in game.inventory:
            possible_commands.append(DropCommand(i))

        # Always add the quit option
        possible_commands.append(QuitCommand())

        # 2. Delegate to the view to show the menu and get the chosen command.
        return view.get_menu_choice(possible_commands)


class CliInputStrategy(InputStrategy):
    """The CLI strategy, updated to return Command objects."""

    def __init__(self):
        # --- NEW: Define all primary verbs and their corresponding command classes ---
        self.verb_map = {
            "take": TakeCommand,
            "get": TakeCommand,
            "drop": DropCommand,
            "inventory": InventoryCommand,
            "inv": InventoryCommand,
            "i": InventoryCommand,
            "look": LookCommand,
            "help": HelpCommand,  # Add the new help verb
            "quit": QuitCommand,
            "exit": QuitCommand,
        }
        self.direction_map = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west",
            "u": "up",
            "d": "down",
            "up": "up",
            "down": "down",
            "north": "north",
            "south": "south",
            "east": "east",
            "west": "west",
        }

    def get_action(self, game: "Game", view: CliView):
        location = game.location

        while True:
            # command = input('\n> ').lower().strip()
            command = view.get_raw_command()

            if not command:
                continue

            parts = command.split(" ", 1)
            verb = parts[0]
            target = parts[1] if len(parts) > 1 else ""

            # 1. Check for Quit
            if verb in ["quit", "exit", "bye"]:
                return QuitCommand()

            # 1. Check for movement
            potential_direction = self.direction_map.get(verb) or (
                verb == "go" and self.direction_map.get(target)
            )
            if potential_direction:
                for transition in location.get_transitions():
                    if transition.direction == potential_direction:
                        return GoCommand(transition)
                print(f"You can't go {potential_direction}.")
                continue

            if verb == "go":
                for transition in location.get_transitions():
                    if target in transition.place.name.lower():
                        return GoCommand(transition)
                print(f"You can't go to a place called '{target}'.")
                continue

            # 2. Check the verb map for other commands
            if verb in self.verb_map:
                command_class = self.verb_map[verb]

                if command_class is LookCommand:
                    return LookCommand(target=target)

                # Handle commands that need a target
                if command_class in [TakeCommand, DropCommand]:
                    if not target:
                        view.render_message(f"What do you want to {verb}?")
                        continue

                    # Logic to find the specific item for Take/Drop...
                    if command_class is TakeCommand:
                        item_found = next(
                            (
                                i
                                for i in location.inventory_items
                                if target in i.name.lower()
                            ),
                            None,
                        )
                        if item_found:
                            return TakeCommand(item_found)

                    if command_class is DropCommand:
                        item_found = next(
                            (i for i in game.inventory if target in i.name.lower()),
                            None,
                        )
                        if item_found:
                            return DropCommand(item_found)

                    if command_class is LookCommand:
                        return LookCommand(
                            target
                        )  # LookCommand handles finding the item

                # Handle commands that don't need a target
                else:
                    return command_class()

            # 3. Check for selectable commands (like "play video games")
            for cmd in location.get_selectable_commands():
                if command in cmd.description.lower():
                    return cmd

            return None
