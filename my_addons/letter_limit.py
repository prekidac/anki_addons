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
from my_addons.config import energy, LETTER


def reached_timebox_wrapper(func) -> callable:
    def wrapper(self, *args, **kwargs):
        if letter_sum(self) - self._start_letter_num >= 10 * LETTER:
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
        nid = obj.db.scalar(
            "select nid from cards where id == ?", card)
        note = obj.db.scalar(
            "select flds from notes where id == ?", nid)

        answer = _answer_from_note(
            field_num, obj.media.strip(note))
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
        if energy <= 0:
            if state == "overview":
                state = "deckBrowser"
                tooltip("Enough")
                print("Enough")
        return func(self, state, *args, **kwargs)
    return wrapper


def stampaj_zadnju(self, *args) -> None:
    print(letter_sum(self.mw.col, last_ans=True))


gui_hooks.reviewer_did_answer_card.append(stampaj_zadnju)
AnkiQt.moveToState = moveToState_wrapper(AnkiQt.moveToState)
Collection.startTimebox = start_timebox_wrapper(Collection.startTimebox)
Collection.timeboxReached = reached_timebox_wrapper(Collection.timeboxReached)
