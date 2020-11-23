from anki.sched import Scheduler

def unbury_block(func):
    def wrapper(*args, **kwargs):
        pass
    return wrapper

# unburyCardsForDeck --> unbury_cards_in_current_deck
# u buducnosti ce biti izmena

Scheduler.unburyCardsForDeck = unbury_block(Scheduler.unburyCardsForDeck) 
Scheduler.unburyCards = unbury_block(Scheduler.unburyCards)