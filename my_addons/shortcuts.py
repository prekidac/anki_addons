from aqt.reviewer import Reviewer
from aqt.qt import *
from anki.hooks import wrap
from aqt import gui_hooks


def my_shortcut_keys(self):
    return [
        ("e", self.mw.onEditCurrent),
        (" ", self.onEnterKey),
        (Qt.Key_Return, self.onEnterKey),
        (Qt.Key_Enter, self.onEnterKey),
        ("r", self.replayAudio),
        (Qt.Key_Tab, self.onTab),
    ]


TAB = False


def my_defaultEase_wrapper(func):
    def wrapper(self):
        global TAB
        if TAB:
            return 1
        else:
            return func(self)
    return wrapper


def onTab(self) -> None:
    if self.state == "question":
        global TAB
        TAB = True
        self._getTypedAnswer()
    elif self.state == "answer":
        self._answerCard(1)

def after_answer(self, card, ease):
    global TAB
    TAB = False

Reviewer._defaultEase = my_defaultEase_wrapper(Reviewer._defaultEase)
Reviewer.onTab = onTab
Reviewer._shortcutKeys = my_shortcut_keys
gui_hooks.reviewer_did_answer_card.append(after_answer)
