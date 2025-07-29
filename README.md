# Python Text Adventure NG (Next Generation)
Welcome to the README for Python Text Adventure NG.
You are standing in a digital workshop, bathed in the glow of your monitor. The air hums with potential. On a workbench before you lies a gleaming new **game engine**.
Your quest, should you choose to accept it, is to use this engine to build a world of your own.
Obvious exits are: **Features**, **Quickstart**, **The Art of World-Building**, **The Great Library**, and **Credits**.
You are carrying: a **healthy dose of curiosity**.

## ✨ > go quickstart
🧭 Quickstart: The First Step
You take your first step on the path of creation. The journey is surprisingly simple.
```bash
# You find a magical scroll with ancient runes. You read them aloud...

# 1. Clone the sacred repository
git clone https://github.com/beachviking/python-text-adventure-ng.git

# 2. Enter the newly-formed directory
cd python-text-adventure-ng

# 3. Use your arcane tool 'uv' to sync your environment*
uv pip sync

# (*If you don't possess 'uv', you may also scribe 'pip install -r requirements.txt')

# 4. Awaken a sample world and bring it to life!
uv run python ship_game.py
```

A portal appears before you, prompting you to choose your interface with the world beyond. Your quest has begun!

## ✨ > go the art of world-building
🗺️ The Art of World-Building: A Creator's Guide
You enter a vast chamber filled with floating blueprints and shimmering maps. This is where you learn to shape reality.
### 1. Scribe Your World's History (my_game.py)
First, you must create a new scroll to contain your world's story.
Your main game class will be the vessel, inheriting its power from the **Game** engine.

```python
from engine.game import Game
# ... other magical imports ...

class MyEpicSaga(Game):
    def __init__(self, input_strategy, view):
        super().__init__('Courage', input_strategy, view)
        self.attributes = PlayerAttributes({'Courage': 100})
        self.location = self._define_world()

    def _define_world(self):
        # ... Here, you will breathe life into your creation ...
        return starting_place
```

### 2. Shape the Land (Place and Item)
With a wave of your hand, you can create **Places** of great wonder and **Items** of power and mystery.

```python
from engine.place import Place
from engine.inventory_item import InventoryItem

castle_gate = Place('Castle Gate', 'Huge iron gates stand before you, barring entry.')
ruby_key = InventoryItem('Ruby Key', 'A small key, warm to the touch, with a ruby at its head.')
guard_post = Place('Guard Post', 'A small, empty guard post.', inventory_items=[ruby_key])
```

### 3. Weave the Paths (Transition)
You connect your **Places** with magical **Transitions**. Some paths are clear (direction='north'), while others are locked, requiring a **key** to pass.

```python
from engine.transition import Transition
# A path from the gate to the guard post, with a return trip created automatically.
castle_gate.add_transitions(Transition(guard_post, direction='east'), reverse=True)
```

### 4. Grant Special Actions (Command)
To allow a hero to perform a unique action, you must forge a **Command**. A **Command** is a self-contained spell, holding the description of the action and the logic to execute it.

```python
from engine.command import Command, CommandResult

class PrayAtAltarCommand(Command):
    def __init__(self):
        super().__init__(description="Pray at the ancient altar")

    def execute(self, game: 'Game') -> CommandResult:
        game.attributes.attribs['Courage'] += 10
        return CommandResult(message="You feel a surge of courage!")

# Place the spell in the world for the hero to find.
chapel.add_events(PrayAtAltarCommand())
```

### 5. The Final Incantation (The Launcher)
To complete your world, you must add the standard summoning ritual to the bottom of your scroll. This allows others to enter the world you have built.

```python
# Copy the if __name__ == '__main__': block from a sample game.
if __name__ == '__main__':
    # ... The standard launcher code ...
```

## ✨ > go features
✨ Features: The Engine's Magic
- **Clean Architecture:** A powerful enchantment (Model-View-Presenter) separates the soul of your world (Model) from its appearance (View).
- **Multiple Interfaces:** A hero may interact with your world via a classic numbered Menu, a modern CLI, or a Whimsical, Colorful Emoji interface.
- **Command Pattern:** All actions are powerful, self-contained Command spells, making your world easy to expand with new magic.
- **Testable Reality:** The engine's structure is designed to be verified by the mystical pytest scribes, ensuring your world remains stable.

## ✨ > go the great library
📚 The Great Library: CLI Commands
You find yourself in a library where every known command is written in a grand tome. You can teach your heroes these words of power.
- Movement: go [direction/place], n, s, e, w, up, down
- Interaction: look, look [item], take [item], drop [item]
- Character: inventory (or i, inv)
- System: help, quit

## ✨ > go credits
🙏 Credits: Acknowledging the Elder Ones

```
You see a pedestal honoring the architects who came before. This engine was forged from the wisdom of an earlier work.
```

This project began as a fork and was heavily refactored from the foundational python-text-adventure by dcbriccetti. We are grateful for the excellent starting point he provided.
You close the README, your mind buzzing with ideas. Your own adventure is ready to be written.