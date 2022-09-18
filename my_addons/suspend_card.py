from aqt import gui_hooks


def suspend(self, card, *args) -> None:
    if card.ivl >= self.mw.col.sched._revConf(card)["maxIvl"]:
        self.mw.col.sched.suspend_cards([self.card.id])
    elif card.reps >= 15:
        print("-- Hard card: ", end="")
        self.mw.col.sched.suspend_cards([card.id])


gui_hooks.reviewer_did_answer_card.append(suspend)
