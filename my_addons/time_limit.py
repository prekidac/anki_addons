from aqt.main import AnkiQt
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from typing import Union, Tuple, Any

try:
    with open('/tmp/norma', 'r') as norma:
        limit = int(norma.readline().strip())
except:
    print("Nema normu")
    limit = 5

limit = limit * 60

def check_time_moveToState(func):
    def wrapper(self, state, *args, **kwargs):
        study_time = self.col.db.first("""select sum(time)/1000 from revlog
            where id > ? """, (self.col.sched.dayCutoff-86400)*1000)
        try:
            if int(study_time[0]) >= limit:
                if state == "overview":
                    state = "deckBrowser"
                    tooltip("Zavrsio.")
        except:
            pass
        func(self, state, *args, **kwargs)
    return wrapper

def check_time_nextCard(func):
    def wrapper(self, *args, **kwargs):
        study_time = self.mw.col.db.first("""select sum(time)/1000 from revlog
            where id > ? """, (self.mw.col.sched.dayCutoff-86400)*1000)
        try:
            if int(study_time[0]) >= limit:
                self.mw.moveToState("overview")
                tooltip("Zavrsio.")
        except:
            pass
        func(self, *args, **kwargs)
    return wrapper

AnkiQt.moveToState = check_time_moveToState(AnkiQt.moveToState)
Reviewer.nextCard = check_time_nextCard(Reviewer.nextCard)