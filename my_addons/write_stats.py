from aqt.main import AnkiQt
import json

OUT_FILE = "/tmp/anki.json"


def unloadProfileAndExit_wrapper(func) -> callable:
    def wrapper(self):
        stats = {}
        stats["new_cards"] = len(self.col.find_cards("is:new"))
        stats["circulation"] = len(self.col.db.list(
            "select id from cards where reps > 0"))
        write_stats(stats)
        return func(self)
    return wrapper


def write_stats(stats: dict) -> None:
    try:
        with open(OUT_FILE, "w") as f:
            json.dump(stats, f, indent=4)
    except:
        print("Write new cards error")


AnkiQt.unloadProfileAndExit = unloadProfileAndExit_wrapper(
    AnkiQt.unloadProfileAndExit)
