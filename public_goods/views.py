from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    body_text = "Introduction text."
    pass


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = [ 'savings']

    timeout_submission = {'consumption': c(Constants.endowment / 2)}


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute."


class Results(Page):
    """Players : How much each has earned"""

    def vars_for_template(self):
        return {
            'total_earnings': self.group.total_contribution * Constants.multiplier,
        }

class Results_control(Page):
    def is_displayed(self):
        if self.participant.vars['treat'] == 'control':
            return True

class Results_t1(Page):
    def is_displayed(self):
        if self.participant.vars['treat'] == 't1':
            return True
class Results_t2(Page):
    def is_displayed(self):
        if self.participant.vars['treat'] == 't2':
            return True
        if self.participant.vars['treat'] == 't3':
            return True

page_sequence = [
    Contribute,
    ResultsWaitPage,
    Results_control,
    Results_t1,
    Results_t2
]
