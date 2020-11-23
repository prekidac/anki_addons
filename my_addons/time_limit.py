import time, copy
from aqt.main import AnkiQt
from aqt.utils import tooltip
from aqt.overview import Overview
from anki.collection import Collection
from typing import Union, Tuple, Any

try:
    with open('/tmp/norma', 'r') as norma:
        limit = int(norma.readline().strip())
except:
    print("Nema normu")
    limit = 4

limit = limit * 60

def onOverview(self):
    study_time= self.col.db.first("""select sum(time)/1000 from revlog
                          where id > ? """,
                          (self.col.sched.dayCutoff-86400)*1000)
    if not study_time[0]:
        study_time[0] = 0
    if int(study_time[0]) >= limit:
        tooltip("Zavrsio.")
    else:
        self.col.reset()
        self.moveToState("overview")


def timeboxReached(self) -> Union[bool, Tuple[Any, int]]:
    "Return (elapsedTime, reps) if timebox reached, or False."
    if not self.conf["timeLim"]:
        # timeboxing disabled
        return False
    elapsed = time.time() - self._startTime
    study_time = self.db.first("""select sum(time)/1000 from revlog
                                where id > ? """,
                                (self.sched.dayCutoff-86400)*1000)
    if not study_time[0]:
        study_time[0] = 0
    if elapsed > self.conf["timeLim"] or int(study_time[0]) >= limit:
        return (self.conf["timeLim"], self.sched.reps - self._startReps)
    return False

def onUnbury(self):
    pass

def onStats(self):
    pass

AnkiQt.onStats = onStats
AnkiQt.onOverview = onOverview
Collection.timeboxReached = timeboxReached
Overview.onUnbury = onUnbury
