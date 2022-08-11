from aqt.main import AnkiQt
import json

OUT_FILE = "/tmp/anki.json"


def unloadProfileAndExit_wrapper(func) -> callable:
    def wrapper(self):
        stats = {}
        stats["new_cards"] = len(self.col.find_cards("is:new"))

        circulation = self.col.db.scalar(
            "select count(id) from cards where reps > 0")
        stats["circulation"] = circulation

        sum_reps = self.col.db.scalar("select sum(reps) from cards")
        stats["average_reps"] = round(sum_reps / circulation)

        again = len(self.col.find_cards("rated:1:1"))
        today = len(self.col.db.list(
            "select distinct cid from revlog where id > ?", (self.col.sched.day_cutoff-86400)*1000))
        if today > 0:
            stats["correct_ratio"] = round((today-again)/today,2)
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
