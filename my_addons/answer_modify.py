from aqt import gui_hooks

EASY_CARD = True
FAIL_ONCE = True


def easy_new_card(ease_tuple, reviewer, card):
    if EASY_CARD and ease_tuple[1] > 1 and card.queue == 0:
        # new card and you know it - answer 4
        print("-- Easy card: ", end="")
        return (True, 4)
    elif FAIL_ONCE and ease_tuple[1] == 1 and card.id in reviewer.mw.col.find_cards("rated:1:1"):
        # fail card only once per day
        print("-- Failed card ", end="")
        return (True, 3)
    return ease_tuple


gui_hooks.reviewer_will_answer_card.append(easy_new_card)
