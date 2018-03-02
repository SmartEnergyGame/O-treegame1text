from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools

doc = """This application provides a survey and introductions based on the answers of the survey."""

class Constants(BaseConstants):
    name_in_url = 'instructions_n_survey'
    players_per_group = None  # 1 group = (4 treatments x 2 people per group)
    num_rounds = 1
    treatments = ['control', 'D', 'DTI']

class unbalance_group_creation(Exception):
    print("Error when creating same size of treatment group")

class Subsession(BaseSubsession):
    def creating_session(self):
        quota = self.session.config['members_per_treatment']
        try:
            if len(self.get_players()) % quota  == 0:
                if self.round_number == 1:
                    current_treatments = Constants.treatments
                    for player in self.get_players():
                        assigned = False
                        while not assigned:
                            treatment = random.choice(current_treatments)
                            counter = 0
                            for p in self.get_players():
                                # counting existing users with treatment before assigning new person with treatment
                                if 'treatment' in p.participant.vars:
                                    if p.participant.vars['treatment'] == treatment:
                                        counter += 1
                                        print('++++++++++++++++++++++++++++++++++++',p.participant.vars['treatment'])
                            if counter < quota:
                                player.participant.vars['treatment'] = treatment
                                player.treatment = treatment
                                assigned = True
            else:
                raise unbalance_group_creation
        except unbalance_group_creation:
            print('++++++++++++++++++++++++++++++++number of members in a treatment must be multiple of the number of participants registered')
            raise unbalance_group_creation


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

