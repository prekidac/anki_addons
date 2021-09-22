from typing import Tuple
from aqt import gui_hooks
from aqt.main import AnkiQt
from aqt.utils import tooltip
from anki.utils import stripHTML
from anki.collection import Collection
from typing import Union
import re
import html
import time
import subprocess
import json

OUT_FILE = "/tmp/anki.json"
LETTER = 4

try:
    p = subprocess.Popen(["energy", "-b"], stdout=subprocess.PIPE)
    energy, err = p.communicate()
    energy = int(energy)
except Exception as e:
    print(e)
    energy = 100


def done_energy(col: Collection) -> int:
    return round((letter_sum(col)-L_START)/LETTER)


def on_load(self) -> None:
    global L_START
    L_START = letter_sum(self)
    print(f"Letter start: {L_START}")


def unloadProfileAndExit_wrapper(func) -> callable:
    def wrapper(self):
        if done_energy(self.col) > 0:
            p = subprocess.Popen(
                ["energy", "-e", "anki", f"{done_energy(self.col)}"])
            p.wait()
        print(f"Letter end: {letter_sum(self.col)}")

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
        self.col.remove_notes(to_sus_nid)
        print("Removed:", num_of_del, "cards")
        return func(self)
    return wrapper


def write_new_cards(new: int) -> None:
    try:
        with open(OUT_FILE, "r") as f:
            routine = json.load(f)
    except:
        routine = {}
    routine["new_cards"] = new
    with open(OUT_FILE, "w") as f:
        json.dump(routine, f, indent=4)


def reached_timebox_wrapper(func) -> callable:
    def wrapper(self, *args, **kwargs):
        if letter_sum(self) - self._start_letter_num >= 10 * LETTER or done_energy(self) >= energy:
            elapsed = time.time() - self._startTime
            print("End:", letter_sum(self))
            return (elapsed, self.sched.reps - self._startReps)
        return func(self, *args, **kwargs)
    return wrapper


def start_timebox_wrapper(func) -> callable:
    def wrapper(self, *args, **kwargs):
        self._start_letter_num = letter_sum(self)
        print("Begin:", self._start_letter_num)
        return func(self, *args, **kwargs)
    return wrapper


def letter_sum(obj: Collection, last_ans: bool = False) -> Union[int, Tuple[str, int]]:
    today_cards = obj.db.list(
        "select cid from revlog where id > ?", (obj.sched.dayCutoff-86400)*1000)

    suma = 0
    for card in today_cards:
        field_num = obj.db.scalar(
            "select ord from cards where id == ?", card)
        if field_num == None:
            # if you review and then change card
            # cid is changed in db
            # but old cid is still in revlog
            # so field_num of old cid is None
            continue
        nid = obj.db.scalar(
            "select nid from cards where id == ?", card)
        note = obj.db.scalar(
            "select flds from notes where id == ?", nid)
        note = re.split('\x1f', note)

        if len(note) > 1:
            answer = note[field_num]
        else:
            answer = _answer_from_note(
                field_num, obj.media.strip(note[0]))
        suma += _letter_count(answer)
    if last_ans:
        return suma, answer
    else:
        return suma


def _letter_count(match_list: list) -> int:
    num = 0
    for match in match_list:
        num += len(match)
    return num


def _answer_from_note(field_num: int, note: str) -> list:
    # Remove HTML tags from note
    # prepisano iz auto_rate_answer addon-a
    note = re.sub("(\n|<br ?/?>|</?div>)+", " ", note)
    note = stripHTML(note)
    note = note.replace(" ", "&nbsp;")
    note = html.unescape(note)
    note = note.replace("\xa0", " ")
    note = note.strip()

    CHARS = r"([^}]*[}]?[^}]+|[^}]*)"
    po = re.compile(r"{{c" + str(field_num + 1) + r"::" + CHARS)
    match_list = po.findall(note)
    po = re.compile(r"(.*)" + "::")
    answers = []
    for i in match_list:
        if po.search(i):
            answers.append(po.search(i).group(1))
        else:
            answers.append(i)
    return answers


def moveToState_wrapper(func: callable) -> callable:
    def wrapper(self, state: str, *args, **kwargs):
        if done_energy(self.col) >= energy:
            if state == "overview":
                state = "deckBrowser"
                tooltip("Enough")
                print("Enough")
        return func(self, state, *args, **kwargs)
    return wrapper


def last_answer(self, card, *args) -> None:
    print(letter_sum(self.mw.col, last_ans=True))


gui_hooks.reviewer_did_answer_card.append(last_answer)
gui_hooks.collection_did_load.append(on_load)
AnkiQt.unloadProfileAndExit = unloadProfileAndExit_wrapper(
    AnkiQt.unloadProfileAndExit)
AnkiQt.moveToState = moveToState_wrapper(AnkiQt.moveToState)
Collection.startTimebox = start_timebox_wrapper(Collection.startTimebox)
Collection.timeboxReached = reached_timebox_wrapper(Collection.timeboxReached)
