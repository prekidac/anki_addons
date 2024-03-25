from aqt import gui_hooks
import re
from aqt import mw
config = mw.addonManager.getConfig(__name__)


def easy_new_card(ease_tuple, reviewer, card):
    if config["hard_and_easy_remove"]:
        if ease_tuple[1] == 2:
            ease_tuple = (True, 1)
        elif ease_tuple[1] == 4:
            ease_tuple = (True, 3)
    if ease_tuple[1] > 1 and card.queue == 0 and config["easy_new_card"]:
        # new card and you know it - answer 4
        print(f"Easy card: {card.id}")
        return (True, 4)
    elif ease_tuple[1] == 1 and card.id in reviewer.mw.col.find_cards("rated:1:1") and config["fail_only_once"]:
        # fail card only once per day
        print(f"Failed card: {card.id}")
        return (True, 3)
    return ease_tuple


gui_hooks.reviewer_will_answer_card.append(easy_new_card)
