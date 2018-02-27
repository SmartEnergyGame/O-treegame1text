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
    name_in_url = 'multi_instructions_n_survey'
    players_per_group = None  # 1 group = (4 treatments x 2 people per group)
    num_rounds = 1
    treatments = ['control', 'D', 'DTI']

class unbalance_group_creation(Exception):
    print("Error when creating same size of treatment group")

class Subsession(BaseSubsession):

    def randomize_groups(self):
        num_groups = len(Constants.treatments)
        num_players = len(self.get_players())
        participants = list(range(1, num_players + 1))
        random.shuffle(participants)
        participants
        distr = len(participants) / num_groups
        if len(participants) % num_groups > 0:  # 7%3 = 1
            pointer = num_groups - 1  # full subgroups to divide the remaining 2
            remaining = len(participants) % num_groups  # 7%3 = 1
            while remaining % pointer > 0:  # 1%2 1%1
                pointer = pointer - 1  # = 1
            add_more = remaining / pointer
            bigger_groups_num = distr + add_more  # original distr + add_more
            small_group = distr
            big_group = [participants[g *bigger_groups_num:g * bigger_groups_num + bigger_groups_num] for g in
                         range(pointer)]
            rest_participants = participants[bigger_groups_num * 1:]  # participants[bigger_groups_num*pointer:]
            small_group = [rest_participants[g * (small_group):g * small_group + small_group] for g in
                           range(num_groups - pointer)]
            return big_group.extend(small_group)
        else :

            structure = [[participants[in_group] for in_group in range(g*int(distr) , g*int(distr)+int(distr))] for g in range(num_groups)]
            return structure

    def creating_session(self):
        if self.round_number == 1:
            new_structure = self.randomize_groups()
            self.set_group_matrix(new_structure)
            current_treatments = Constants.treatments
            used_treatments = []
            for g in self.get_groups():
            #while len(used_treatments) < 3:
                print(used_treatments)
                treatment = random.choice([ t for t in current_treatments if t not in used_treatments])
                used_treatments.append(treatment)
                for p in g.get_players():
                    p.participant.vars['treatment'] =  treatment


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.IntegerField(doc="Question 1", label="How much does each player have to invest into the conservation account, on average, for each round to meet the goal?", choices= ["$0", "$0.5", "$1"])

    q2 = models.CharField(doc="Question 2", label="Assuming the goal has been met, total payments from the conservation account are equal to what amount?", choices = [['t1',"The total in the conservation account "],['t1',"Two times the total in the conservation account "], ['',"Three times the total in the conservation account "]])

    q3 = models.CharField(doc="Question 3", label="Please assume that the goal of $24 has been contributed to the conservation account. If there are 6 players in the game, how much will each player receive as a bonus for meeting the conservation account goal?  Each Player will receive $")

    q4 = models.CharField(doc="Question 4", label="Assume $30 has been contributed to the conservation account by the end of the experiment, and you have personally invested a total of $5 over the 8 rounds, leaving $11 in your private account. How much money will you receive at the end of the experiment, after the conservation account bonus incentive has been paid? My payout is $")


    q5 = models.CharField(doc="Question 4", label="Lease assume that the goal of $24 has NOT been contributed to the conservation account and you have invested a total of $5 in the 8 rounds, leaving $11 in your private account. How much money will you receive at the end of the experiment.  My payout is $")


    q6 = models.CharField(doc = "Question 6", label="Is it possible to meet the conservation account goal even if one player does not contribute to the goal at all? ", choices = ["Yes", "No"])

    treatment = models.CharField(doc="Treatment")
    injunctive_norm_type = models.CharField(initial='undefined_IT')

    def role(self):
        if ((self.participant.vars['treatment'] == 'DTI')):
            self.participant.vars['role'] = self.q2
        else:
            self.participant.vars['role'] = 'undefined_IT'
        return self.participant.vars['role']

