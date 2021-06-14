from os import lstat
from aqt.main import AnkiQt
from my_addons.config import LETTER, OUT_FILE
from anki.collection import Collection
from my_addons.letter_limit import letter_sum
import subprocess
import json


def _loadCollection(self) -> None:
    cpath = self.pm.collectionPath()
    self.col = Collection(cpath, backend=self.backend, log=True)
    self.setEnabled(True)

    global L_START
    L_START = letter_sum(self.col)


def unloadProfileAndExit(self) -> None:
    e = round((letter_sum(self.col)-L_START)/LETTER)
    if e > 0:
        p = subprocess.Popen(
            ["energy", "-e", "anki", f"{e}"])
        p.wait()

    new = self.col.db.scalar(
        "select count() from cards where type == 0 and queue != -2")
    write_new_cards(new)
    all_sus_nid = self.col.db.list(
        "select nid from cards where queue == -1 group by nid")
    today_cid = self.col.db.list(
        "select cid from revlog where id > ? ", (self.col.sched.dayCutoff-86400)*1000)
    today_nid = []
    for cid in today_cid:
        today_nid.append(self.col.db.scalar(
            "select nid from cards where id == ?", cid))
    to_sus_nid = []
    num_of_del = 0
    for nid in all_sus_nid:
        nid_queues = self.col.db.list(
            "select queue from cards where nid == " + str(nid))
        for queue in nid_queues:
            if queue != -1:
                break
        else:
            if nid not in today_nid:
                num_of_del += len(nid_queues)
                to_sus_nid.append(nid)
    print("Removed:", num_of_del, "cards")
    self.col.remove_notes(to_sus_nid)

    self.unloadProfile(self.cleanupAndExit)


def write_new_cards(new: int) -> None:
    try:
        with open(OUT_FILE, "r") as f:
            routine = json.load(f)
    except:
        routine = {}
    routine["new_cards"] = new
    with open(OUT_FILE, "w") as f:
        json.dump(routine, f, indent=4)


AnkiQt.unloadProfileAndExit = unloadProfileAndExit
AnkiQt._loadCollection = _loadCollection
