from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class Instructions(Page):
    def vars_for_template(self):
        participant = self.participant
        return {
            'redemption_code': participant.label or participant.code,
        }
class survey(Page):
    form_model = models.Player
    form_fields = ['q1', 'q2']

page_sequence = [Instructions,survey]
