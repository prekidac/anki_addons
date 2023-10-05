from aqt import gui_hooks
from aqt.main import AnkiQt
from aqt.utils import tooltip
from anki.collection import Collection
import time
from aqt import mw
config = mw.addonManager.getConfig(__name__)


def on_load(self) -> None:
    global CARDS_PER_DAY
    CARDS_PER_DAY = config["limit_number"]


def reached_timebox_wrapper(func) -> callable:
    def wrapper(self, *args, **kwargs):
        if not cards_left(self):
            elapsed = time.time() - self._startTime
            return (elapsed, self.sched.reps - self._startReps)
        return func(self, *args, **kwargs)
    return wrapper


def moveToState_wrapper(func: callable) -> callable:
    def wrapper(self, state: str, *args, **kwargs):
        if state == "overview" and not cards_left(self.col):
            state = "deckBrowser"
            tooltip("Enough")
        return func(self, state, *args, **kwargs)
    return wrapper


def cards_left(col: Collection) -> bool:
    if not config["limit"]:
        return True
    col.sched._reset_counts()
    left = CARDS_PER_DAY - len(col.find_cards("rated:1:1"))
    if left > 0 or col.sched.revCount > 0 or col.sched._immediate_learn_count > 0:
        return True
    else:
        return False


gui_hooks.collection_did_load.append(on_load)
AnkiQt.moveToState = moveToState_wrapper(AnkiQt.moveToState)
Collection.timeboxReached = reached_timebox_wrapper(Collection.timeboxReached)
