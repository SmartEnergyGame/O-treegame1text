from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

#define global variables


class Intro(Page):
    def vars_for_template(self):
        all_players = len(self.group.get_players())
        vars = { 'players_in_group' : all_players ,
                 'other_players':all_players-1,
                 'endowment':c(self.session.config['endowment']).to_real_world_currency(self.session),
                 'goal':self.session.config['community_goal_decimal']*100,
                 'goal_financial':c(self.session.config['community_goal_decimal']*all_players*self.session.config['endowment']).to_real_world_currency(self.session),
                 'share': c(self.session.config['community_goal_decimal']*self.session.config['endowment']).to_real_world_currency(self.session)

                 }
        return vars

class Intro_part2(Page):
    def vars_for_template(self):
        all_players = len(self.group.get_players())
        vars = { 'players_in_group' : all_players ,
                 'other_players':all_players-1,
                 'endowment':c(self.session.config['endowment']).to_real_world_currency(self.session),
                 'goal':self.session.config['community_goal_decimal']*100,
                 'goal_financial':c(.5*8*all_players).to_real_world_currency(self.session),
                 'share': c(self.session.config['community_goal_decimal']*self.session.config['endowment']).to_real_world_currency(self.session)

                 }
        return vars
                 
class survey(Page):
    form_model = models.Player
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']

    def before_next_page(self):
        self.player.role()
        self.player.total_correct_ans()

class SurveyResults(Page):
    form_model = models.Player
    def vars_for_template(self):
        ans = self.player.check_answers()
        return {'answers' : ans}

    def before_next_page(self):
        self.participant.vars['correct_answers'] = self.player.correct_answers
        print(self.participant.vars['correct_answers'])

class AssignationWaitPage(WaitPage):

    body_text = "Please wait for the other participants to make their decision!"

page_sequence = [Intro,Intro_part2, survey, SurveyResults, AssignationWaitPage]
