from aqt.main import AnkiQt
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from typing import Union, Tuple, Any

try:
    with open('/tmp/norma', 'r') as norma:
        limit = int(norma.readline().strip())
except:
    print("Nema normu")
    limit = 100

limit = limit / 20

def check_time_moveToState(func: callable) -> callable:
    def wrapper(self, state: str, *args, **kwargs):
        study_time = self.col.db.scalar("""select sum(time)/1000 from revlog
            where id > ? """, (self.col.sched.dayCutoff-86400)*1000)
        try:
            if int(study_time) >= limit:
                if state == "overview":
                    state = "deckBrowser"
                    tooltip("Zavrsio.")
        except:
            pass
        func(self, state, *args, **kwargs)
    return wrapper

def check_time_nextCard(func: callable) -> callable:
    def wrapper(self, *args, **kwargs):
        study_time = self.mw.col.db.scalar("""select sum(time)/1000 from revlog
            where id > ? """, (self.mw.col.sched.dayCutoff-86400)*1000)
        try:
            if int(study_time) >= limit:
                self.mw.moveToState("overview")
                tooltip("Zavrsio.")
        except:
            pass
        func(self, *args, **kwargs)
    return wrapper

AnkiQt.moveToState = check_time_moveToState(AnkiQt.moveToState)
Reviewer.nextCard = check_time_nextCard(Reviewer.nextCard)