from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class mr_Intro(Page):
    def vars_for_template(self):
        return { 'players_in_group' : self.session.config['members_per_treatment'],
                 'other_players':self.session.config['members_per_treatment']-1,
                 'endowment':c(self.session.config['endowment']).to_real_world_currency(self.session),
                 'goal':self.session.config['community_goal_decimal']*100,
                 'goal_financial':c(self.session.config['community_goal_decimal']*self.session.config['members_per_treatment']*self.session.config['endowment']).to_real_world_currency(self.session),
                 'share': c(self.session.config['community_goal_decimal']*self.session.config['endowment']).to_real_world_currency(self.session)

                 }


class mr_survey(Page):
    form_model = models.Player
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
    def before_next_page(self):
        self.player.role()

class AssignationWaitPage(WaitPage):

    body_text = "Waiting for other participants to complete survey."

page_sequence = [mr_Intro,mr_survey, AssignationWaitPage]
