from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Post_survey(Page):
    form_model = models.Player
    form_fields = ['q011', 'q021', 'q031', 'q041', 'q051', 'q061', 'q071', 'q081', 'q091', 'q101', 'q111', 'q121',
                   'q131', 'q141']

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass

class Final_page(Page):
    def vars_for_template(self):
            group_size = len(self.group.get_players())
            group_savings = self.session.config['endowment']*group_size - sum([ p.participant.vars['endowment'] for p in self.group.get_players()])
            return {
                'endowment': self.player.participant.vars['endowment'].to_real_world_currency(self.session),
                'group_savings': group_savings,
                'goal': c(8 * len(
                    [p for p in self.group.in_round(1).get_players()]) * .5).to_real_world_currency(
                    self.session)

            }

page_sequence = [
    Final_page,
    Post_survey
]
