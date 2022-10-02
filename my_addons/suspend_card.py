from aqt import gui_hooks
import re

def answer(col, card) -> str:
    nid = col.db.scalar(
        "select nid from cards where id == ?", card.id)
    note = col.db.scalar(
        "select flds from notes where id == ?", nid)
    note = re.split('\x1f', note)
    if len(note) > 1:
        return note[card.ord]
    else:
        CHARS = r"([^}]*[}]?[^}]+|[^}]*)"
        po = re.compile(r"{{c" + str(card.ord + 1) + r"::" + CHARS)
        match_list = po.findall(note[0])
        po = re.compile(r"(.*)" + "::")
        answers = []
        for i in match_list:
            if po.search(i):
                answers.append(po.search(i).group(1))
            else:
                answers.append(i)
        return " ".join(answers)

def suspend(self, card, *args) -> None:
    if card.ivl >= self.mw.col.sched._revConf(card)["maxIvl"]:
        self.mw.col.sched.suspend_cards([card.id])
    elif card.reps >= num_of_steps(self.mw.col, card):
        print(f"Hard card: {answer(self.mw.col, card)}")
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
