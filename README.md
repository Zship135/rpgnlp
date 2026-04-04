# rpgnlp

A natural language parser for RPG text commands. Extracts structured data — actions, subjects, directions, instruments, modifiers, and topics — from free-form player input.

## Installation

```bash
pip install rpgnlp
```

After installing, download the required spaCy language model:

```bash
python -m spacy download en_core_web_md
```

You also need the NLTK tokenizer data (downloaded automatically on first use, or manually):

```python
import nltk
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt_tab')
```

## Quick Start

```python
from rpgnlp import NLPEngine

engine = NLPEngine()

result = engine.run("attack the goblin with a sword")
print(result)
# {
#     "action": "attack",
#     "subject": "goblin",
#     "direction": "",
#     "instrument": [{"name": "sword", "quantity": 1}],
#     "modifiers": [],
#     "topic": ""
# }
```

## Output Fields

| Field | Type | Description |
|---|---|---|
| `action` | `str` | Canonical action (e.g., `"attack"`, `"travel"`, `"speak"`) |
| `subject` | `str` | Target noun phrase (e.g., `"goblin"`, `"red door"`) |
| `direction` | `str` | Cardinal/compound direction (e.g., `"north"`, `"south east"`) |
| `instrument` | `list[dict]` | Instruments with name and quantity |
| `modifiers` | `list[str]` | Adverbs or manner words (e.g., `"quickly"`, `"haste"`) |
| `topic` | `str` | Conversation topic after "about" (e.g., `"plan"`) |

## Supported Actions

| Action | Examples |
|---|---|
| `attack` | attack, hit, strike, slash, stab, shoot, kick |
| `light_attack` | poke, prod, tap, flick, slap, nip |
| `heavy_attack` | smash, crush, demolish, obliterate, shatter |
| `travel` | go, run, walk, sprint, climb, swim, fly |
| `speak` | talk, say, ask, whisper, shout, demand |
| `inspect` | look, examine, observe, study, check |
| `search` | search, hunt, investigate, scout, seek |
| `defend` | block, parry, dodge, guard, protect |
| `use` | use, activate, equip, drink, eat, open |
| `take` | take, grab, loot, steal, collect |
| `drop` | drop, place, put, discard, give |
| `cast` | cast, conjure, summon, enchant, heal |
| `sneak` | sneak, hide, lurk, prowl, shadow |
| `rest` | rest, sleep, camp, meditate, wait |
| `trade` | buy, sell, barter, haggle, shop |

## Examples

```python
engine = NLPEngine()

# Movement with direction
engine.run("run north east")
# action: "travel", direction: "north east"

# Speech with topic
engine.run("tell the guard about the plan")
# action: "speak", subject: "guard", topic: "plan"

# Multiple instruments with quantities
engine.run("attack the goblin with two daggers and a shield")
# action: "attack", subject: "goblin",
# instrument: [{"name": "daggers", "quantity": 2}, {"name": "shield", "quantity": 1}]

# Modifiers
engine.run("run south with haste")
# action: "travel", direction: "south", modifiers: ["haste"]

# Compound actions (split by "and" or "then")
results = engine.run("go north then attack the troll")
# Returns the last action; compound actions are processed sequentially
```

## Requirements

- Python >= 3.9
- spaCy with `en_core_web_md` model
- NLTK

## License

MIT
