from .event import Event
from .inventory_item import InventoryItem
from .transition import Transition
from .activity import Activity
from .player_attributes import PlayerAttributes
from .command import Command

OPPOSITE_DIRECTIONS = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
    "up": "down",
    "down": "up",
    "in": "out",
    "out": "in",
    "northeast": "southwest",
    "southwest": "northeast",
    "northwest": "southeast",
    "southeast": "northwest",
}


class Place:
    """
    A location in the game.
    """

    name: str
    description: str
    events: list[Event]
    inventory_items: list[InventoryItem]
    transitions: list[Transition]

    def __init__(
        self,
        name: str,
        description: str = "",
        events: list[Event] = None,
        inventory_items: list[InventoryItem] = None,
    ):
        self.name = name
        self.description = description if description else f"You are in {name}."
        self.events = events if events else []
        self.inventory_items = inventory_items if inventory_items else []
        self.transitions = []

    def add_events(self, *events: Event):
        self.events.extend(events)

    def add_activities(self, *activities: Activity):
        """A convenience method for adding activities."""
        self.add_events(*activities)

    def process_events(self, attributes: PlayerAttributes):
        # Local import to avoid circular dependencies.

        for event in self.events:
            if isinstance(event, Command):
                continue  # Skips to the next item in the loop

            # ONLY process the event if it is NOT an Activity.
            if not isinstance(event, Activity):
                event.process(attributes)

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def add_transitions(self, *targets, reverse=False):
        """
        Adds transitions to this place. If reverse=True, it will now create
        a return transition with the correct opposite direction.
        """
        from .transition import Transition

        for target in targets:
            # Add the forward transition (this part is the same)
            if isinstance(target, Place):
                self.add_transition(Transition(target))
            elif isinstance(target, Transition):
                self.add_transition(target)
            else:
                raise TypeError(
                    f"add_transitions requires Place or Transition, not {type(target)}"
                )

            if reverse:
                target_place = (
                    target.place if isinstance(target, Transition) else target
                )

                reverse_direction = None
                # Check if the original was a Transition object AND it had a direction
                if isinstance(target, Transition) and target.direction:
                    # Find the opposite direction from our new dictionary
                    reverse_direction = OPPOSITE_DIRECTIONS.get(target.direction)

                # Create the reverse transition, passing the direction if we found one
                target_place.add_transition(
                    Transition(self, direction=reverse_direction)
                )

    def get_transitions(self) -> list[Transition]:
        return self.transitions

    def get_selectable_commands(self) -> list[Command]:
        """
        Filters the master event list for commands that are selectable
        by the player in a menu.
        """
        # A command is selectable if it's a Command and has a description.
        return [
            cmd for cmd in self.events if isinstance(cmd, Command) and cmd.description
        ]
