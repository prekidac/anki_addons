from os import lstat
from aqt.main import AnkiQt
from my_addons.config import KOEF, write_new_cards
from anki.collection import Collection
from my_addons.letter_limit import answer_from_fields, letter_count
import subprocess

L_START = 0

def _loadCollection(self) -> None:
    cpath = self.pm.collectionPath()
    self.col = Collection(cpath, backend=self.backend, log=True)
    self.setEnabled(True)

    today_cards = self.col.db.list(
        "select cid from revlog where id > ?", (self.col.sched.dayCutoff-86400)*1000)
    suma = 0
    for card in today_cards:
        field_num = self.col.db.scalar(
            "select ord from cards where id == ?", card)
        nid = self.col.db.scalar(
            "select nid from cards where id == ?", card)
        fields = self.col.db.scalar(
            "select flds from notes where id == ?", nid)

        try:
            answer = answer_from_fields(
                field_num, self.col.media.strip(fields))
            suma += letter_count(answer)
        except Exception as e:
            print(e)
    
    global L_START
    L_START = suma


def unloadProfileAndExit(self) -> None:

    today_cards = self.col.db.list(
        "select cid from revlog where id > ?", (self.col.sched.dayCutoff-86400)*1000)
    suma = 0
    for card in today_cards:
        field_num = self.col.db.scalar(
            "select ord from cards where id == ?", card)
        nid = self.col.db.scalar(
            "select nid from cards where id == ?", card)
        fields = self.col.db.scalar(
            "select flds from notes where id == ?", nid)

        answer = answer_from_fields(
            field_num, self.col.media.strip(fields))
        suma += letter_count(answer)

    if suma != L_START:
        p = subprocess.Popen(["energy", "anki", f"{round((suma-L_START)/KOEF)}"])
        p.wait()


    new = self.col.db.scalar("select count() from cards where type == 0 and queue != -2")
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
    print("Izbrisano:", num_of_del, "kartica")
    self.col.remove_notes(to_sus_nid)

    self.unloadProfile(self.cleanupAndExit)


AnkiQt.unloadProfileAndExit = unloadProfileAndExit
AnkiQt._loadCollection = _loadCollection