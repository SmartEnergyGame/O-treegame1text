from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
    This application provides a survey and introductions based on the answers of the survey.
"""

class Constants(BaseConstants):
    name_in_url = 'instructions_n_survey'
    players_per_group = 2
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    q1 = models.CharField(doc="Question 1")
    q2 = models.IntegerField(doc="Question 2")

    def role(self):
        if (self.q1 == "e") and (self.q2 == 1):
            self.participant.vars['injunctive_norm'] = 'eco'
        else:
            self.participant.vars['injunctive_norm'] = 'type1'
        return self.participant.vars['injunctive_norm'];

