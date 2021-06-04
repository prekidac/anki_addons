import json
from pathlib import Path
import subprocess

OUT_FILE = "/tmp/anki.json"
KOEF = 8

try:
    p = subprocess.Popen(["energy", "-r"], stdout=subprocess.PIPE)
    energy, err = p.communicate()
    energy = int(energy)
except Exception as e:
    print(e)
    energy = 100
limit = energy * KOEF


def write_new_cards(new: int) -> None:
    try:
        with open(OUT_FILE, "r") as f:
            routine = json.load(f)
    except:
        routine = {}
    routine["new_cards"] = new
    with open(OUT_FILE, "w") as f:
        json.dump(routine, f, indent=4)
