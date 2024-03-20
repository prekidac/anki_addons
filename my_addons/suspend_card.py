from aqt import gui_hooks
import re
import subprocess
from aqt import mw
config = mw.addonManager.getConfig(__name__)

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
    hc = 0
    if card.ivl >= config["maxIvl"]:
        self.mw.col.sched.suspend_cards([card.id])
    elif card.reps >= num_of_steps(self.mw.col, card):
        print(f"Hard card: {answer(self.mw.col, card)}")
        hc = 1
        self.mw.col.sched.suspend_cards([card.id])
    try:
        p = subprocess.Popen(["hard_card", "-a", f"{hc}"])
        p.wait()
    except:
        print("No hard_card app")

def num_of_steps(col, card) -> int:
    AGAIN = config["hard_card_fail_steps"]
    fct = card.factor / 1000
    new = 2
    review = 0
    ivl = 1
    while ivl < config["maxIvl"]:
        review += 1
        ivl = int(max(ivl * fct, ivl + 2))
    return AGAIN + new + review

gui_hooks.reviewer_did_answer_card.append(suspend)
