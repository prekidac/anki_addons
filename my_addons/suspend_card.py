from aqt import gui_hooks
from aqt import mw
from aqt.main import AnkiQt
config = mw.addonManager.getConfig(__name__)


def unloadProfileAndExit_wrapper(func) -> callable:
    def wrapper(self):
        must_be_suspended = self.col.db.list(
            "select id from cards where ivl >= ? and queue != -1", config["maximum_interval"]
        )
        if must_be_suspended:
            self.col.sched.suspend_cards(must_be_suspended)
            print(f"Must be suspended: {must_be_suspended}")

        return func(self)
    return wrapper


def suspend(self, card, *args) -> None:
    if card.ivl >= config["maximum_interval"]:
        print(f"Suspended: {card.id}")
        self.mw.col.sched.suspend_cards([card.id])
    elif card.reps >= num_of_steps(self.mw.col, card):
        print(f"Hard card: {card.id}")
        self.mw.col.sched.suspend_cards([card.id])

def num_of_steps(col, card) -> int:
    AGAIN = config["hard_card_fail_steps"]
    fct = card.factor / 1000
    new = 2
    review = 0
    ivl = 1
    while ivl < config["maximum_interval"]:
        review += 1
        ivl = int(max(ivl * fct, ivl + 2))
    return AGAIN + new + review

gui_hooks.reviewer_did_answer_card.append(suspend)
AnkiQt.unloadProfileAndExit = unloadProfileAndExit_wrapper(
    AnkiQt.unloadProfileAndExit)
