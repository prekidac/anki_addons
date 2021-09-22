from aqt import gui_hooks


def suspend(self, card, *args) -> None:
    if card.ivl >= self.mw.col.sched._revConf(card)["maxIvl"]:
        self.mw.col.sched.suspend_cards([self.card.id])


gui_hooks.reviewer_did_answer_card.append(suspend)
