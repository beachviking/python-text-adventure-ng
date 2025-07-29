from random import randint
from time import sleep

from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.player_attributes import PlayerAttributes
from engine.transition import Transition
from engine.strategies import MenuInputStrategy, CliInputStrategy
from engine.command import Command, CommandResult
from engine.view import CliView, MenuView, ColoramaView


class PlayVideoGamesCommand(Command):
    def __init__(self):
        # --- Pass the description to the parent class ---
        super().__init__(description="Play video games")

    def execute(self, game: "Game") -> CommandResult:
        gaming_skill_change = 5
        happiness_change = randint(-10, 20)

        game.attributes.attribs["Gaming Skill"] += gaming_skill_change
        game.attributes.attribs["Happiness"] += happiness_change

        returnString = f"You sit down and take the controller. You"

        
        if happiness_change > 0:
            return CommandResult(
                message=f"{returnString} won! You gain {gaming_skill_change} gaming skill and {happiness_change} happiness.",
                location_changed=False,
            )
        
        if happiness_change < 0:
            return CommandResult(
                message=f"{returnString} lost. You lose {gaming_skill_change} gaming skill and {happiness_change} happiness.",
                location_changed=False,
            )

        return CommandResult(message=f"{returnString} tied.", location_changed=False)


class YoungSheldon(Game):
    introduction: str
    attributes: PlayerAttributes

    def __init__(self, input_strategy, view):
        super().__init__("Happiness", input_strategy, view)
        self.introduction = "Welcome to Young Sheldon Adventure"
        self.attributes = PlayerAttributes(
            {
                "Health": 100,
                "Happiness": 100,
                "Gaming Skill": 0,
                "Confidence": 100,
            }
        )

        home: Place = self._define_game()
        self.location = home

    def _define_game(self) -> Place:
        home = Place("Home", "You are at home.")
        relaxation_event = Event(0.75, "You play with your trains.", 5)
        relaxation_event.add_else_events(Event(1, "Missy plays loud sad music.", -20))
        feynman_poster_event = Event(0.3, "You talk to your Richard Feynman poster", 10)
        home.add_events(relaxation_event, feynman_poster_event)

        billys = Place("Billy Sparks’s House")
        chicken_event = Event(0.3, "Billy’s chicken scares you", -10)
        chicken_event.add_else_events(Event(1, "Billy says something kind", 5))
        billys.add_events(chicken_event)

        meemaws = Place("Meemaw’s house")
        meemaws.add_events(
            Event(0.4, "Meemaw makes cookies", 20),
            Event(0.3, "We play video games", {"Gaming Skill": 10}),
            Event(0.05, "Meemaw is mad at you", -10),
        )

        sunday_school = Place("Sunday School")
        sunday_school.add_events(
            Event(0.2, "Paige makes you mad", -20),
            Event(0.3, "You win an argument with Pastor Jeff", {"Confidence": 20}),
            Event(0.2, "Billy says something funny", 5),
        )

        university = Place("East Texas Tech")
        university.add_events(
            Event(0.1, "Your mother embarrasses you", -5),
            Event(0.6, "You are glad to be at your place of higher learning", 5),
        )

        key = InventoryItem(
            "Private dorm room key",
            description='It’s a small, standard-issue brass key. A small tag reads "RM 2B".',
        )
        hagemeyers = Place("President Hagemeyer’s Office", inventory_items=[key])
        dorm_room = Place(
            "Your Dorm Room", events=[Event(0.9, "You have a nice rest", 15)]
        )
        friends_dorm_room = Place("Oscar and Darren’s Dorm Room")
        friends_dorm_room.add_events(
            Event(0.3, "Paige drops by and bums everybody out", -10, max_occurrences=1),
            Event(0.2, "You eat too much junk food and barf", -20),
        )
        friends_dorm_room.add_events(PlayVideoGamesCommand())

        sturgis_class = Place(
            "Dr. Sturgis’s class", "Your front row seat in Dr. Sturgis’s class"
        )
        linkletters_office = Place("Dr. Linkletter’s office")
        linkletters_office.add_events(
            Event(1, "Dr. Linkletter is not happy to see you", -10)
        )

        home.add_transitions(
            Transition(meemaws, direction="north"),
            Transition(university, direction="south"),
            Transition(billys, direction="west"),
            Transition(sunday_school, direction="east"),
            reverse=True,  # The reverse transitions will still be created automatically
        )
        university.add_transitions(
            hagemeyers, sturgis_class, linkletters_office, reverse=True
        )
        university.add_transitions(
            Transition(dorm_room, key=key),
            Transition(friends_dorm_room, key=key),
            reverse=True,
        )

        return home


if __name__ == "__main__":
    mode = ""
    while mode not in ["1", "2"]:
        mode = input(
            "Choose interaction mode:\n1. Menu (Original)\n2. CLI (New)\nEnter 1 or 2: "
        )

    if mode == "1":
        strategy = MenuInputStrategy()
        view = MenuView()
    else:  # mode == "2"
        strategy = CliInputStrategy()
        # view = CliView()
        view = ColoramaView()  # Assuming ColorCliView is defined in engine/view.py

    # Create the game instance with the chosen pair
    game = YoungSheldon(input_strategy=strategy, view=view)
    game.play()
