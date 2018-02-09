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
    name_in_url = 'single_treatment_survey'
    players_per_group = None  # 1 group = (4 treatments x 2 people per group)
    num_rounds = 1
    treatments = ['control', 'D', 'DTI']

class unbalance_group_creation(Exception):
    print("Error when creating same size of treatment group")

class Subsession(BaseSubsession):

    def creating_session(self):
        treatments = self.session.config['single_treatment']
        if self.round_number == 1:
                    for player in self.get_players():
                        player.participant.vars['treatment'] = treatments
                        player.treatment = treatments

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.CharField(doc="Question 1", label="Where do you supposedly live?")
    q2 = models.CharField(doc="Question 2", label="Which is more concerning to you with regards to the effects of climate change on people?", choices = [['type1',"health problems affecting you and your family"],['type1',"health problems affecting your community"]])
    treatment = models.CharField(doc="Treatment")
    injunctive_norm_type = models.CharField(initial='undefined_IT')
    def role(self):
        if ((self.participant.vars['treatment'] == 'DTI')):
            self.participant.vars['role'] = self.q2
        else:
            self.participant.vars['role'] = 'undefined_IT'
        return self.participant.vars['role']

