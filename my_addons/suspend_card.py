from aqt import gui_hooks


def suspend(self, card, *args) -> None:
    if card.ivl >= self.mw.col.sched._revConf(card)["maxIvl"]:
        self.mw.col.sched.suspend_cards([self.card.id])
    elif card.reps >= num_of_steps(self.mw.col, card):
        print("-- Hard card")
        self.mw.col.sched.suspend_cards([card.id])

def num_of_steps(col, card) -> int:
    AGAIN = 10
    revConf = col.sched._revConf(card)
    fct = card.factor / 1000
    newConf = col.sched._newConf(card)
    new = len(newConf["delays"])
    review = 0
    ivl = 1
    while ivl < revConf["maxIvl"]:
        review += 1
        ivl = int(max(ivl * fct, ivl + 2))
    return AGAIN + new + review

gui_hooks.reviewer_did_answer_card.append(suspend)
