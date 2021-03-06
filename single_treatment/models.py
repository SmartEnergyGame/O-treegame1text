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
                        player.participant.vars['correct_answers'] = 0

class Group(BaseGroup):
    pass



class Player(BasePlayer):
    #choices1q = [c(0).to_real_world_currency(BasePlayer.session), c(1*2), c(1*4)]
    def check_answersP2(self):
        correct_answer = "Correct!"
        if self.q4 == "$26.00":
            q4_feedback = [1,"Your answer was: "+ self.q4 , correct_answer]

        else:
            q4_feedback = [0,"Your answer was: "+ self.q4 , "In this scenario, the group has met the threshold for the incentive from the conservation account. This means you get an equal share of the $90.00 group incentive ($30.00 x 3), or $15.00. In addition, you keep the $11.00 remaining in your private account. Your total payout is $15.00 + $11.00 = $26.00"]
        if self.q5 == "$11.00":
            q5_feedback = [1,"Your answer was: "+ self.q5 , correct_answer]

        else:
            q5_feedback = [0,"Your answer was: "+ self.q5 , "Because the group did not reach the threshold in the conservation account for the group incentive, there is no group bonus. You will receive only the money remaining in your private account = $11.00."]
        if self.q6 == "Yes":
            q6_feedback = [1,"Your answer was: "+ self.q6 , correct_answer]

        else:
            q6_feedback = [0,"Your answer was: "+ self.q6 , "All players do not have to contribute to the conservation account to meet the goal. For example, if 1 player does not donate, the other players can still meet the goal by contributing slightly more than $0.50 per round on average."]

        res = [q4_feedback,q5_feedback,q6_feedback]
        return res

    def check_answers(self):
        correct_answer = "Correct!"

        if self.q1 == "$0.50":
            q1_feedback = [1,"Your answer was: "+ self.q1 , correct_answer]

        else:
            q1_feedback = [0,"Your answer was: "+ self.q1 , "The energy conservation goal is $" + str(8*.5*(len(self.get_others_in_subsession())+1)) + ", so each player has to contribute $0.50 each round, on average, to meet the goal."]
        if self.q2 == 'Three times the total in the conservation account ':
            q2_feedback = [1,"Your answer was: "+ self.q2 , correct_answer]

        else:
            q2_feedback = [0,"Your answer was: "+ self.q2 , "The total incentive payment to the group is equal to three times the total contributions in the conservation account at the end of the game."]
        if self.q3 == "$12.00":
            q3_feedback = [1,"Your answer was: "+ self.q3 , correct_answer]

        else:
            q3_feedback = [0,"Your answer was: "+ self.q3 , "Because the 6 players have met the threshold for the conservation account, they will receive a share of the group incentive. Because the group incentive is equal to three times the account total, the total incentive payment is $72.00. Each player receives an equal share of that incentive, or $12.00 each."]

        res = [q1_feedback,q2_feedback,q3_feedback]
        return res


    def total_correct_ans(self):
        res = self.check_answers()
        correct = sum([a[0] for a in res])
        res2 = self.check_answersP2()
        correct2 = sum([a[0] for a in res2])
        print(correct)
        self.participant.vars['correct_answers'] = correct + correct2
        self.correct_answers = correct + correct2

    correct_answers = models.IntegerField(initial=0)
    q1 = models.CharField(
        doc="1. How much does each player have to invest into the conservation account, on average, for each round to meet the goal?",
        label="1. How much does each player have to invest into the conservation account, on average, for each round to meet the goal?",
        choices = ["$0.00", "$0.50", "$1.00"],
        widget=widgets.RadioSelectHorizontal,
    )
    q2 = models.CharField(
         doc="2. Assume the goal has been met, total payments from the conservation account are equal to what amount?",
         label="2. Assume the goal has been met, total payments from the conservation account are equal to what amount?",
         choices = [
             "The total in the conservation account ",
             "Two times the total in the conservation account ",
             "Three times the total in the conservation account "
             ], 
         widget=widgets.RadioSelect,
         )
    q3 = models.CharField(
        doc="3. Assume the 6 players in the game have contributed $24.00 to the conservation account, meeting the account goal. How much will each player receive as a bonus for meeting the conservation account goal? Each player will receive: ",
        label="3. Assume the 6 players in the game have contributed $24.00 to the conservation account, meeting the account goal. How much will each player receive as a bonus for meeting the conservation account goal? Each player will receive: ",
        choices=[
            "$11.00",
            "$12.00",
            "$24.00"
        ],widget=widgets.RadioSelectHorizontal,

    )
    
    q4 = models.CharField(
        doc="4. Assume there are 6 players in the game and they have contributed $30.00 to the conservation account by the end of the experiment, and you have personally invested a total of $5.00 over the 8 rounds, leaving $11.00 in your private account. How much money will you receive at the end of the experiment, after the conservation account bonus incentive has been paid? My payout is: ",
        label="4. Assume there are 6 players in the game and they have contributed $30.00 to the conservation account by the end of the experiment, and you have personally invested a total of $5.00 over the 8 rounds, leaving $11.00 in your private account. How much money will you receive at the end of the experiment, after the conservation account bonus incentive has been paid? My payout is: "
        , choices=[
            "$15.00",
            "$11.00",
            "$26.00"
        ],widget=widgets.RadioSelectHorizontal,
    )

    
    q5 = models.CharField(
        doc="5. Assume that the goal of $24.00 has NOT been contributed to the conservation account and you have invested a total of $5.00 in the 8 rounds, leaving $11.00 in your private account. How much money will you receive at the end of the experiment. My payout is $: ",
        label="5. Assume that the goal of $24.00 has NOT been contributed to the conservation account and you have invested a total of $5.00 in the 8 rounds, leaving $11.00 in your private account. How much money will you receive at the end of the experiment. My payout is $: "
        , choices=[
            "$5.00",
            "$11.00",
            "$26.00"
        ],widget=widgets.RadioSelectHorizontal,
    )
    
    q6 = models.CharField(
        doc = "6. Is it possible to meet the conservation account goal even if one player does not contribute to the goal at all? ",
        label="6. Is it possible to meet the conservation account goal even if one player does not contribute to the goal at all? ",
        choices = ["Yes","No"],
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
    

