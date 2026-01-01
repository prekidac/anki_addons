import copy
from anki.decks import DeckManager
from anki.consts import NEW_CARDS_DUE
from aqt import gui_hooks
from aqt import mw
config = mw.addonManager.getConfig(__name__)



defaultConf = {
    "id": 1,
    "name": "Default",
    "new": {
        "delays": [10, 1200],
        "ints": [1, 4, 7],  # 7 is not currently used
        "initialFactor": 1500,
        "separate": True,
        "order": NEW_CARDS_DUE,
        "perDay": config["failed_cards"],
        # may not be set on old decks
        "bury": True,
    },
    "lapse": {
        "delays": [60],
        "mult": 1,
        "minInt": 1,
        "leechFails": 5,
        # type 0=suspend, 1=tagonly
        "leechAction": 0,
    },
    "rev": {
        "perDay": 200,
        "ease4": 1.3,
        "fuzz": 0.05,
        "minSpace": 1,  # not currently used
        "ivlFct": 1,
        "maxIvl": config["maximum_interval"],
        # may not be set on old decks
        "bury": True,
        "hardFactor": 1.2,
    },
    "maxTaken": 60,
    "timer": 0,
    "autoplay": True,
    "replayq": True,
    "mod": 0,
    "usn": 0,
    "newMix": 1,
}


def my_default(self):
    self.mw.col.decks.update_config(defaultConf)


gui_hooks.deck_options_did_load.append(my_default)