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
    #choices1q = [c(0).to_real_world_currency(BasePlayer.session), c(1*2), c(1*4)]
    
    q1 = models.IntegerField(
        doc="Question 1", 
        label="How much does each player have to invest into the conservation account, on average, for each round to meet the goal?",
        choices = [[0,"$ 0"],[1,"$ 0.5"],[0,"$ 1.0"]],
        widget=widgets.RadioSelectHorizontal,
    )
    q2 = models.IntegerField(
         doc="Question 2",
         label="Assuming the goal has been met, total payments from the conservation account are equal to what amount?", 
         choices = [
             [0,"The total in the conservation account "],
             [0,"Two times the total in the conservation account "],
             [1,"Three times the total in the conservation account "]
             ], 
         widget=widgets.RadioSelect,
         )
    q3 = models.IntegerField(
        doc="Question 3", 
        label="Please assume that the goal of $24 has been contributed to the conservation account."
              " If there are 6 players in the game,"
              " how much will each player receive as a bonus for meeting the conservation account goal?  "
              "Each Player will receive $",
        choices=[
            [0, "$ 11"],
            [1, "$ 12"],
            [0, "$ 24"]
        ],widget=widgets.RadioSelectHorizontal,

    )
    
    q4 = models.IntegerField(
        doc="Question 4",
        label="Assume $30 has been contributed to the conservation account by the end of the experiment, and you have personally invested a total of $5 over the 8 rounds, leaving $11 in your private account. How much money will you receive at the end of the experiment, after the conservation account bonus incentive has been paid? My payout is $"
        , choices=[
            [0, "$ 15"],
            [1, "$ 11"],
            [0, "$ 26"]
        ],widget=widgets.RadioSelectHorizontal,
    )

    
    q5 = models.IntegerField(
        doc="Question 5",
        label="Let's assume that the goal of $24 has NOT been contributed to the conservation account and you have invested a total of $5 in the 8 rounds, leaving $11 in your private account. How much money will you receive at the end of the experiment.  My payout is $"
        , choices=[
            [0, "$ 5"],
            [0, "$ 11"],
            [1, "$ 24"]
        ],widget=widgets.RadioSelectHorizontal,
    )
    
    q6 = models.IntegerField(
        doc = "Question 6", 
        label="Is it possible to meet the conservation account goal even if one player does not contribute to the goal at all? ", 
        choices = [[1,"Yes"],[0,"No"]],
        widget=widgets.RadioSelectHorizontal,
    )

    treatment = models.CharField(doc="Treatment")
    injunctive_norm_type = models.CharField(initial='undefined_IT')
    def role(self):
        if ((self.participant.vars['treatment'] == 'DTI')):
            self.participant.vars['role'] = 'DTI'
        else:
            self.participant.vars['role'] = 'undefined_IT'
        return self.participant.vars['role']
    

