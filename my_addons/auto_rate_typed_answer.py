import html
import re

from anki.hooks import wrap
from anki.utils import stripHTML
from aqt.reviewer import Reviewer
from aqt import mw

IGNORE_CASE = True

def answer_from_field(self, fieldcontent):
    cor = self.mw.col.media.strip(fieldcontent)
    cor = re.sub("(\n|<br ?/?>|</?div>)+", " ", cor)
    cor = stripHTML(cor)
    # ensure we don't chomp multiple whitespace
    cor = cor.replace(" ", "&nbsp;")
    cor = html.unescape(cor)
    cor = cor.replace("\xa0", " ")
    cor = cor.strip()
    return cor


def does_it_match(self, given):
    # self.typeCorrect contains the contents of a field
    if given == answer_from_field(self, self.typeCorrect):
        return True
    elif IGNORE_CASE:
        if given.lower() == answer_from_field(self, self.typeCorrect).lower():
            return True
    return False


def my_defaultEase(self, _old):
    if self.typedAnswer:
        return 1
    else:
        return _old(self)
Reviewer._defaultEase = wrap(Reviewer._defaultEase, my_defaultEase, "around")


def myAutoAnswerCorrect(self):
    if self.typedAnswer:
        if does_it_match(self, self.typedAnswer):
            cnt = self.mw.col.sched.answerButtons(mw.reviewer.card)  # Get button count
            if cnt == 2:
                self._answerCard(2)
            elif cnt == 3:
                self._answerCard(2)
            else:
                self._answerCard(3)
Reviewer._showAnswer = wrap(Reviewer._showAnswer, myAutoAnswerCorrect)
