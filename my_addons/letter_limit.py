from aqt.main import AnkiQt
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from typing import Union, Tuple, Any
from anki.utils import stripHTML
import re, html

try:
    with open('/tmp/norma', 'r') as norma:
        limit = int(norma.readline().strip())
except:
    print("Nema normu")
    limit = 5

limit = limit * 100

def check_time_moveToState(func: callable) -> callable:
    def wrapper(self, state: str, *args, **kwargs):
        today_cards = self.col.db.list("""select cid from revlog
            where id > ? """, (self.col.sched.dayCutoff-86400)*1000)
        
        suma = 0
        for card in today_cards:
            field_number = self.col.db.scalar("""select ord from cards where id == ? """, card)
            note = self.col.db.scalar("""select nid from cards where id == ? """, card)
            fields = self.col.db.scalar("""select flds from notes where id == ?""", note)

            cor = self.col.media.strip(fields)
            cor = re.sub("(\n|<br ?/?>|</?div>)+", " ", cor)
            cor = stripHTML(cor)
            # ensure we don't chomp multiple whitespace
            cor = cor.replace(" ", "&nbsp;")
            cor = html.unescape(cor)
            cor = cor.replace("\xa0", " ")
            fields = cor.strip()

            po = re.compile(r"({{c" + str(field_number + 1) + r"::)" + r"([\w\d\s,;.\-()'\"]*)")
            suma += len(po.search(fields).group(2))

        if suma >= limit:
            if state == "overview":
                state = "deckBrowser"
                tooltip("Zavrsio.")
        func(self, state, *args, **kwargs)
    return wrapper

def check_time_nextCard(func: callable) -> callable:
    def wrapper(self, *args, **kwargs):
        today_cards = self.mw.col.db.list("""select cid from revlog
            where id > ? """, (self.mw.col.sched.dayCutoff-86400)*1000)
        
        suma = 0
        for card in today_cards:
            field_number = self.mw.col.db.scalar("""select ord from cards where id == ? """, card)
            note = self.mw.col.db.scalar("""select nid from cards where id == ? """, card)
            fields = self.mw.col.db.scalar("""select flds from notes where id == ?""", note)

            cor = self.mw.col.media.strip(fields)
            cor = re.sub("(\n|<br ?/?>|</?div>)+", " ", cor)
            cor = stripHTML(cor)
            # ensure we don't chomp multiple whitespace
            cor = cor.replace(" ", "&nbsp;")
            cor = html.unescape(cor)
            cor = cor.replace("\xa0", " ")
            fields = cor.strip()

            po = re.compile(r"({{c" + str(field_number + 1) + r"::)" + r"([\w\d\s,;.\-()'\"]*)")
            suma += len(po.search(fields).group(2))
            print(fields, suma)

        if suma >= limit:
            if state == "overview":
                state = "deckBrowser"
                tooltip("Zavrsio.")

        func(self, *args, **kwargs)
    return wrapper

AnkiQt.moveToState = check_time_moveToState(AnkiQt.moveToState)
Reviewer.nextCard = check_time_nextCard(Reviewer.nextCard)