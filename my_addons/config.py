import json
from pathlib import Path

CONF_FILE = str(Path.home()) + "/.local/share/routines/config.json"
OUT_FILE = "/tmp/anki.json"
KOEF = 9

try:
    with open(CONF_FILE, "r") as f:
        routine = json.load(f)
        limit = routine["limit"]
except:
    print("Nema limit")
    limit = 100
limit = limit * KOEF


def write_done(done: int) -> None:
    try:
        with open(OUT_FILE, "r") as f:
            routine = json.load(f)
    except:
        routine = {}
    routine["done"] = int(done / KOEF)
    with open(OUT_FILE, "w") as f:
        json.dump(routine, f, indent=4)


def write_new_cards(new: int) -> None:
    try:
        with open(OUT_FILE, "r") as f:
            routine = json.load(f)
    except:
        routine = {}
    routine["new_cards"] = new
    with open(OUT_FILE, "w") as f:
        json.dump(routine, f, indent=4)
