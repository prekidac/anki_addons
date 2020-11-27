from aqt.main import AnkiQt
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from anki.utils import stripHTML
from anki.collection import *
import re, html
import time

try:
    with open('/tmp/norma', 'r') as norma:
        limit = int(norma.readline().strip())
except:
    print("Nema normu")
    limit = 100 

KOEF = 10 # reci/% energije
limit = limit * KOEF 

def reached_timebox_wrapper(func) -> callable:
    def wrapper(self, *args, **kwargs):
        today_cards = self.db.list("""select cid from revlog
            where id > ? """, (self.sched.dayCutoff-86400)*1000)

        suma = 0
        for card in today_cards:
            field_num = self.db.scalar("""select ord from cards where id == ? """, card)
            nid = self.db.scalar("""select nid from cards where id == ? """, card)
            fields = self.db.scalar("""select flds from notes where id == ?""", nid)

            try:
                answer = answer_from_fields(field_num, self.media.strip(fields))
                suma += letter_count(answer)
            except:
                pass

        if suma - self._start_letter_num >= 10 * KOEF:
            elapsed = time.time() - self._startTime
            print("Kraj bloka:", suma, answer)
            return (elapsed, self.sched.reps - self._startReps)
        return func(self, *args, **kwargs)
    return wrapper

def start_timebox_wrapper(func) -> callable:
    def wrapper(self, *args, **kwargs):
        today_cards = self.db.list("""select cid from revlog
            where id > ? """, (self.sched.dayCutoff-86400)*1000)
        
        suma = 0
        for card in today_cards:
            field_num = self.db.scalar("""select ord from cards where id == ? """, card)
            nid = self.db.scalar("""select nid from cards where id == ? """, card)
            fields = self.db.scalar("""select flds from notes where id == ?""", nid)

            try:
                answer = answer_from_fields(field_num, self.media.strip(fields))
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
    """
    Remove HTML tags from note
    """
    # prepisano iz auto_rate_answer addon-a
    fields = re.sub("(\n|<br ?/?>|</?div>)+", " ", fields)
    fields = stripHTML(fields)
    fields = fields.replace(" ", "&nbsp;")
    fields = html.unescape(fields)
    fields = fields.replace("\xa0", " ")
    fields = fields.strip()

    po = re.compile(r"{{c" + str(field_num + 1) + r"::" + r"([\w\d\s,;.\-()'\"]*)")
    return po.findall(fields)

def check_time_moveToState(func: callable) -> callable:
    def wrapper(self, state: str, *args, **kwargs):
        today_cards = self.col.db.list("""select cid from revlog
            where id > ? """, (self.col.sched.dayCutoff-86400)*1000)
        
        suma = 0
        for card in today_cards:
            field_num = self.col.db.scalar("""select ord from cards where id == ? """, card)
            nid = self.col.db.scalar("""select nid from cards where id == ? """, card)
            fields = self.col.db.scalar("""select flds from notes where id == ?""", nid)

            try:
                answer = answer_from_fields(field_num, self.col.media.strip(fields))
                suma += letter_count(answer)
            except:
                pass
            
        if suma >= limit:
            if state == "overview":
                state = "deckBrowser"
                tooltip("Zavrsio.")
        return func(self, state, *args, **kwargs)
    return wrapper

def check_time_nextCard(func: callable) -> callable:
    def wrapper(self, *args, **kwargs):
        today_cards = self.mw.col.db.list("""select cid from revlog
            where id > ? """, (self.mw.col.sched.dayCutoff-86400)*1000)
        
        suma = 0
        for card in today_cards:
            field_num = self.mw.col.db.scalar("""select ord from cards where id == ? """, card)
            nid = self.mw.col.db.scalar("""select nid from cards where id == ? """, card)
            fields = self.mw.col.db.scalar("""select flds from notes where id == ?""", nid)

            try:
                answer = answer_from_fields(field_num, self.mw.col.media.strip(fields))
                suma += letter_count(answer)
            except:
                pass

        if suma >= limit:
            print("Zavrsio: ", suma)
            self.mw.moveToState("deckBrowser")

        return func(self, *args, **kwargs)
    return wrapper

def stampaj_uradjenu(self) -> None:
    """Stampa zadnji odgovor i ukupnu sumu slova"""
    today_cards = self.mw.col.db.list("""select cid from revlog
        where id > ? """, (self.mw.col.sched.dayCutoff-86400)*1000)
    
    suma = 0
    for card in today_cards:
        field_num = self.mw.col.db.scalar("""select ord from cards where id == ? """, card)
        nid = self.mw.col.db.scalar("""select nid from cards where id == ? """, card)
        fields = self.mw.col.db.scalar("""select flds from notes where id == ?""", nid)

        try:
            answer = answer_from_fields(field_num, self.mw.col.media.strip(fields))
            suma += letter_count(answer)
        except:
            pass

    try:
        print(answer, str(suma))
    except:
        print("Nema danasnjih kartica")

def _answerCard(self, ease: int) -> None:
    "Reschedule card and show next."
    if self.mw.state != "review":
        # showing resetRequired screen; ignore key
        return
    if self.state != "answer":
        return
    if self.mw.col.sched.answerButtons(self.card) < ease:
        return
    proceed, ease = gui_hooks.reviewer_will_answer_card(
        (True, ease), self, self.card
    )
    if not proceed:
        return
    self.mw.col.sched.answerCard(self.card, ease)
    gui_hooks.reviewer_did_answer_card(self, self.card, ease)
    self._answeredIds.append(self.card.id)
    self.mw.autosave()
    self.stampaj_uradjenu() # dodata func
    self.nextCard()

AnkiQt.moveToState = check_time_moveToState(AnkiQt.moveToState)
Reviewer.nextCard = check_time_nextCard(Reviewer.nextCard)
Reviewer._answerCard = _answerCard
Reviewer.stampaj_uradjenu = stampaj_uradjenu
Collection.startTimebox = start_timebox_wrapper(Collection.startTimebox)
Collection.timeboxReached = reached_timebox_wrapper(Collection.timeboxReached)