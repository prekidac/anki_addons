from aqt import gui_hooks
import re
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

def easy_new_card(ease_tuple, reviewer, card):
    if not config["answer_modify"]:
        return ease_tuple
    if ease_tuple[1] > 1 and card.queue == 0:
        # new card and you know it - answer 4
        print(f"Easy card: {answer(reviewer.mw.col, card)}")
        return (True, 4)
    elif ease_tuple[1] == 1 and card.id in reviewer.mw.col.find_cards("rated:1:1"):
        # fail card only once per day
        print(f"Failed card: {answer(reviewer.mw.col, card)}")
        return (True, 3)
    return ease_tuple


gui_hooks.reviewer_will_answer_card.append(easy_new_card)
