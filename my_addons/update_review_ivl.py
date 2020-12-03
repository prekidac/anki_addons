from anki.cards import Card
from anki.sched import Scheduler


def upReIv(self, card: Card, ease: int) -> None:
    # no fuzz
    card.ivl = min(
        max(self._nextRevIvl(card, ease), card.ivl + 1),
        self._revConf(card)["maxIvl"],
    )
    if card.ivl >= self._revConf(card)["maxIvl"]:
        card.queue = -1


Scheduler._updateRevIvl = upReIv
