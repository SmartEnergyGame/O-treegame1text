from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools

doc = """
    This application provides a survey and introductions based on the answers of the survey.
"""

class Constants(BaseConstants):
    name_in_url = 'instructions_n_survey'
    players_per_group = 2  # 1 group = (4 treatments x 2 people per group)
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
          treatments = itertools.cycle(['control', 'D', 'DTI'])
          if self.round_number == 1:
          	 self.group_randomly()
             for g in self.get_groups():
                 treat = next(treatments)
                 for p in g.get_players():
                     p.participant.vars['treatment'] = treat
                     p.treatment = treat


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.CharField(doc="Question 1")
    q2 = models.IntegerField(doc="Question 2")
    treatment = models.CharField(doc="Treatment")
    injunctive_norm_type = models.CharField(initial='undefined_IT')
    def role(self):
        if ((self.participant.vars['treatment'] == 'DTI')) and (self.q2 == 1):
            self.participant.vars['injunctive_norm_type'] = 'eco'
        elif ((self.participant.vars['treatment'] == 'DTI')) and (self.q2 == 2):
            self.participant.vars['injunctive_norm_type'] = 'type1'
        elif ((self.participant.vars['treatment'] == 'DTI')) and (self.q2 == 3):
            self.participant.vars['injunctive_norm_type'] = 'type2'
        else:
            self.participant.vars['injunctive_norm_type'] = 'undefined_IT'
        return self.participant.vars['injunctive_norm_type']

