from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class Instructions(Page):
    def is_displayed(self):
        if self.participant.vars['injunctive_norm'] == "type1":
            return True

class InstructionsT1(Page):
    def is_displayed(self):
        if self.participant.vars['injunctive_norm'] == "type2":
            return True
class InstructionsT2(Page):
    def is_displayed(self):
        if self.participant.vars['injunctive_norm'] == "type3":
            return True
class InstructionsT3(Page):
    def is_displayed(self):
        if self.participant.vars['injunctive_norm'] == "ecologic_inj_role_participant":
            return True
class survey(Page):
    form_model = models.Player
    form_fields = ['q1', 'q2']
    def before_next_page(self):
        self.player.role()

class AssignationWaitPage(WaitPage):

    body_text = "Waiting for other participants to complete survey."

page_sequence = [survey, AssignationWaitPage,Instructions]
