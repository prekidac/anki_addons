from aqt.reviewer import Reviewer
from aqt.qt import Qt 


def my_shortcut_keys(self):
    return [
        ("e", self.mw.onEditCurrent),
        (" ", self.onEnterKey),
        (Qt.Key.Key_Return, self.onEnterKey),
        (Qt.Key.Key_Enter, self.onEnterKey),
        ("r", self.replayAudio),
        (Qt.Key.Key_Tab, self.onTab),
        ("j", self.onTab),
        ("k", self.onEnterKey)
    ]


def onTab(self) -> None:
    if self.state == "answer":
        self._answerCard(1)


Reviewer.onTab = onTab
Reviewer._shortcutKeys = my_shortcut_keys
