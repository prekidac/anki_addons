from aqt.main import AnkiQt
import json

OUT_FILE = "/tmp/anki.json"


def unloadProfileAndExit_wrapper(func) -> callable:
    def wrapper(self):
        new = self.col.db.scalar(
            "select count() from cards where type == 0 and queue != -2")
        write_new_cards(new)
        return func(self)
    return wrapper


def write_new_cards(new: int) -> None:
    out = {}
    out["new_cards"] = new
    try:
        with open(OUT_FILE, "w") as f:
            json.dump(out, f, indent=4)
    except:
        print("Write new cards error")

AnkiQt.unloadProfileAndExit = unloadProfileAndExit_wrapper(
    AnkiQt.unloadProfileAndExit)