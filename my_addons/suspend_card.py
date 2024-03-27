from aqt import gui_hooks
from aqt import mw
config = mw.addonManager.getConfig(__name__)


def suspend(self, card, *args) -> None:
    hc = 0
    if card.ivl >= config["maximum_interval"]:
        self.mw.col.sched.suspend_cards([card.id])
    elif card.reps >= num_of_steps(self.mw.col, card):
        print(f"Hard card: {card.id}")
        hc = 1
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
