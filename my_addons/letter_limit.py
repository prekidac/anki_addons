from aqt import gui_hooks
from aqt.main import AnkiQt
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from anki.utils import stripHTML
from anki.collection import Collection
import re
import html
import copy
import time
import json
from pathlib import Path

CONF_FILE = str(Path.home()) + "/.local/share/routine.json"

try:
    with open(CONF_FILE, "r") as f:
        routine = json.load(f)
        limit = routine["limit"]
except:
    print("Nema limit")
    limit = 100

KOEF = 9
limit = limit * KOEF


def reached_timebox_wrapper(func) -> callable:
    def wrapper(self, *args, **kwargs):
        today_cards = self.db.list(
            "select cid from revlog where id > ?", (self.sched.dayCutoff-86400)*1000)

        suma = 0
        for card in today_cards:
            field_num = self.db.scalar(
                "select ord from cards where id == ?", card)
            nid = self.db.scalar(
                "select nid from cards where id == ?", card)
            fields = self.db.scalar(
                "select flds from notes where id == ?", nid)

            try:
                answer = answer_from_fields(
                    field_num, self.media.strip(fields))
                suma += letter_count(answer)
            except:
                pass

        if suma - self._start_letter_num >= 10 * KOEF:
            elapsed = time.time() - self._startTime
            print("Kraj bloka:", suma)
            return (elapsed, self.sched.reps - self._startReps)
        return func(self, *args, **kwargs)
    return wrapper


def start_timebox_wrapper(func) -> callable:
    def wrapper(self, *args, **kwargs):
        today_cards = self.db.list(
            "select cid from revlog where id > ?", (self.sched.dayCutoff-86400)*1000)

        suma = 0
        for card in today_cards:
            field_num = self.db.scalar(
                "select ord from cards where id == ?", card)
            nid = self.db.scalar(
                "select nid from cards where id == ?", card)
            fields = self.db.scalar(
                "select flds from notes where id == ?", nid)

            try:
                answer = answer_from_fields(
                    field_num, self.media.strip(fields))
                suma += letter_count(answer)
            except:
                pass

        self._start_letter_num = suma
        print("Pocetak:", self._start_letter_num)
        return func(self, *args, **kwargs)
    return wrapper


def letter_count(match_list: list) -> int:
    num = 0
    for match in match_list:
        num += len(match)
    return num


def answer_from_fields(field_num: int, fields: str) -> list:
    """Remove HTML tags from note"""
    # prepisano iz auto_rate_answer addon-a
    fields = re.sub("(\n|<br ?/?>|</?div>)+", " ", fields)
    fields = stripHTML(fields)
    fields = fields.replace(" ", "&nbsp;")
    fields = html.unescape(fields)
    fields = fields.replace("\xa0", " ")
    fields = fields.strip()

    CHARS = r"([\w\d\s,;:.\-()\[\]’'\"]*)"
    po = re.compile(r"{{c" + str(field_num + 1) + r"::" + CHARS)
    match_list = po.findall(fields)
    po = re.compile(CHARS + "::")
    for i in copy.copy(match_list):
        index = match_list.index(i)
        try:
            match_list[index] = po.search(match_list[index]).group(1)
        except:
            pass
    return match_list


def moveToState_wrapper(func: callable) -> callable:
    def wrapper(self, state: str, *args, **kwargs):
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
            except:
                pass

        if suma >= limit:
            if state == "overview":
                state = "deckBrowser"
                tooltip("Dosta.")
                print("Dosta:", suma)
        return func(self, state, *args, **kwargs)
    return wrapper


def nextCard_wrapper(func: callable) -> callable:
    def wrapper(self, *args, **kwargs):
        today_cards = self.mw.col.db.list(
            "select cid from revlog where id > ?", (self.mw.col.sched.dayCutoff-86400)*1000)

        suma = 0
        for card in today_cards:
            field_num = self.mw.col.db.scalar(
                "select ord from cards where id == ?", card)
            nid = self.mw.col.db.scalar(
                "select nid from cards where id == ?", card)
            fields = self.mw.col.db.scalar(
                "select flds from notes where id == ?", nid)

            try:
                answer = answer_from_fields(
                    field_num, self.mw.col.media.strip(fields))
                suma += letter_count(answer)
            except:
                pass

        if suma >= limit:
            print("Zavrsio: ", suma)
            return self.mw.moveToState("deckBrowser")
        return func(self, *args, **kwargs)
    return wrapper


def stampaj_zadnju(self, *args) -> None:
    """Stampa zadnji odgovor i ukupnu sumu slova"""
    today_cards = self.mw.col.db.list(
        "select cid from revlog where id > ?", (self.mw.col.sched.dayCutoff-86400)*1000)

    suma = 0
    for card in today_cards:
        field_num = self.mw.col.db.scalar(
            "select ord from cards where id == ?", card)
        nid = self.mw.col.db.scalar(
            "select nid from cards where id == ?", card)
        fields = self.mw.col.db.scalar(
            "select flds from notes where id == ?", nid)

        try:
            answer = answer_from_fields(
                field_num, self.mw.col.media.strip(fields))
            suma += letter_count(answer)
        except:
            pass

    try:
        print(answer, suma)
    except:
        print("Nema danasnjih kartica")


gui_hooks.reviewer_did_answer_card.append(stampaj_zadnju)
AnkiQt.moveToState = moveToState_wrapper(AnkiQt.moveToState)
Reviewer.nextCard = nextCard_wrapper(Reviewer.nextCard)
Collection.startTimebox = start_timebox_wrapper(Collection.startTimebox)
Collection.timeboxReached = reached_timebox_wrapper(Collection.timeboxReached)
