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
    form_fields = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9","q10", "q11","q12", 'q021', 'q031', 'q041','q042',
                   'q051', 'q061', 'q071', 'q081', 'q091', 'q101', 'q111','q112', 'q121', 'q131', 'q141']

    def vars_for_template(self):

        questions_1 = [self.player.q1, self.player.q2, self.player.q3, self.player.q4, self.player.q5, self.player.q6,
                       self.player.q7, self.player.q8, self.player.q9, self.player.q10, self.player.q11,
                       self.player.q12]
        shuffle(questions_1)
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12 = questions_1
        a1 = Post_survey.form_fields[0]
        return {

            'a1': a1,
            'a2': a2,
            'a3': a3,
            'a4': a4,
            'a5': a5,
            'a6': a6,
            'a7': a7,
            'a8': a8,
            'a9': a9,
            'a10': a10,
            'a11': a11,
            'a12': a12,
            'list':questions_1

        }

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass

class LastPage(Page):
    form_model = models.Player

    def vars_for_template(self):
     return {'total': self.player.total_payment.to_real_world_currency(self.session),}


page_sequence = [
    Final_page,
    Post_survey,
    LastPage
]
