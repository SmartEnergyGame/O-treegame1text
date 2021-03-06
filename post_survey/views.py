from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from random import shuffle


class Final_page(Page):

    def vars_for_template(self):
            group_size = len(self.group.get_players())
            group_savings = self.session.config['endowment']*group_size - sum([ p.participant.vars['endowment'] for p in self.group.get_players()])
            self.group.get_bonus()
            ca =  self.player.participant.vars['endowment']
            return {
                'goal': c(8 * len(
                    [p for p in self.group.in_round(1).get_players()]) * .5).to_real_world_currency(
                    self.session),
                'endowment': self.player.participant.vars['endowment'].to_real_world_currency(self.session),
                'group_savings': (group_savings).to_real_world_currency(self.session),
                's': self.player.bonus.to_real_world_currency(self.session) ,
                'total': self.player.total_payment.to_real_world_currency(self.session),
                'ans': c(self.player.participant.vars['correct_answers']*.5).to_real_world_currency(self.session)
            }


class Post_survey(Page):
    form_model = models.Player
    form_fields = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9","q10", "q11","q12"]

class Post_surveyP2(Page):
    form_model = models.Player
    form_fields = ['q151','q021', 'q031', 'q041','q042',
                   'q051','q052']
class Post_surveyP3(Page):
    form_model = models.Player
    form_fields = ['q061', 'q071', 'q081', 'q082', 'q091']
class Post_surveyP4(Page):
    form_model = models.Player
    form_fields = [ 'q101', 'q111','q112', 'q121', 'q131', 'q141']
class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass
    body_text = "Please wait for the other participants to make their decision!"

class LastPage(Page):
    form_model = models.Player

    def vars_for_template(self):
     return {'total': self.player.total_payment.to_real_world_currency(self.session),}



page_sequence = [
    Final_page,
    Post_survey,
    Post_surveyP2,
    Post_surveyP3,
    Post_surveyP4,
    LastPage
]
