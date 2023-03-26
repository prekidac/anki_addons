from aqt.reviewer import Reviewer
from aqt.qt import Qt 


def my_shortcut_keys(self):
    return [
        ("e", self.mw.onEditCurrent),
        (" ", self.onEnterKey),
        (Qt.Key.Key_Return, self.onEnterKey),
        (Qt.Key.Key_Enter, self.onEnterKey),
        ("m", self.showContextMenu),
        ("r", self.replayAudio),
        (Qt.Key.Key_F5, self.replayAudio),
        *(
            (f"Ctrl+{flag.index}", self.set_flag_func(flag.index))
            for flag in self.mw.flags.all()
        ),
        ("*", self.toggle_mark_on_current_note),
        ("=", self.bury_current_note),
        ("-", self.bury_current_card),
        ("!", self.suspend_current_note),
        ("@", self.suspend_current_card),
        #("Ctrl+Alt+N", self.forget_current_card),
        #("Ctrl+Alt+E", self.on_create_copy),
        ("Ctrl+Delete", self.delete_current_note),
        ("Ctrl+Shift+D", self.on_set_due),
        ("v", self.onReplayRecorded),
        ("Shift+v", self.onRecordVoice),
        ("o", self.onOptions),
        ("i", self.on_card_info),
        ("Ctrl+Alt+i", self.on_previous_card_info),
        ("1", lambda: self._answerCard(1)),
        ("2", lambda: self._answerCard(2)),
        ("3", lambda: self._answerCard(3)),
        ("4", lambda: self._answerCard(4)),
        ("5", self.on_pause_audio),
        ("6", self.on_seek_backward),
        ("7", self.on_seek_forward),
        (Qt.Key.Key_Tab, self.onTab),
        ("j", self.onTab),
        ("k", self.onEnterKey)
    ]


def onTab(self) -> None:
    if self.state == "answer":
        self._answerCard(1)


Reviewer.onTab = onTab
Reviewer._shortcutKeys = my_shortcut_keys
