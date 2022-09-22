import copy
from anki.decks import DeckManager
from anki.consts import NEW_CARDS_DUE

defaultConf = {
    "name": "Default",
    "new": {
        "delays": [10, 1200],
        "ints": [1, 4, 7],  # 7 is not currently used
        "initialFactor": 1500,
        "separate": True,
        "order": NEW_CARDS_DUE,
        "perDay": 10,
        # may not be set on old decks
        "bury": True,
    },
    "lapse": {
        "delays": [60],
        "mult": 100,
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
        "maxIvl": 5,
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
}


def restoreToDefault(self, conf):
    oldOrder = conf["new"]["order"]
    new = copy.deepcopy(defaultConf)
    new["id"] = conf["id"]
    new["name"] = conf["name"]
    self.update_config(new)
    # if it was previously randomized, resort
    if not oldOrder:
        self.col.sched.resortConf(new)


DeckManager.restore_to_default = restoreToDefault
