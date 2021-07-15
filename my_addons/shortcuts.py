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
        (Qt.Key_F5, self.replayAudio),
        ("Ctrl+1", lambda: self.setFlag(1)),
        ("Ctrl+2", lambda: self.setFlag(2)),
        ("Ctrl+3", lambda: self.setFlag(3)),
        ("Ctrl+4", lambda: self.setFlag(4)),
        ("Ctrl+0", lambda: self.setFlag(0)),
        ("*", self.onMark),
        ("=", self.onBuryNote),
        ("-", self.onBuryCard),
        ("!", self.onSuspend),
        ("@", self.onSuspendCard),
        ("Ctrl+Delete", self.onDelete),
        ("v", self.onReplayRecorded),
        ("Shift+v", self.onRecordVoice),
        ("o", self.onOptions),
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
