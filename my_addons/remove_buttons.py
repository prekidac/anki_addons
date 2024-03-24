from aqt.reviewer import Reviewer
from aqt.utils import (
    askUserDialog,
    tr
)
from aqt.qt import QMessageBox
from aqt.overview import Overview

def check_timebox(self) -> bool:
        "True if answering should be aborted."
        elapsed = self.mw.col.timeboxReached()
        if elapsed:
            assert not isinstance(elapsed, bool)
            part1 = tr.studying_card_studied_in(count=elapsed[1])
            mins = int(round(elapsed[0] / 60))
            part2 = tr.studying_minute(count=mins)
            diag = askUserDialog(f"{part1} {part2}", ["Finish"])
            diag.setIcon(QMessageBox.Icon.Information)
            diag.run()
            self.mw.moveToState("deckBrowser")
            return True
        return False

def on_unbury(func):
    pass


Overview.on_unbury = on_unbury
Reviewer.check_timebox = check_timebox