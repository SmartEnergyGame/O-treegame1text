from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools

doc = """Public good game section (Rounds and feedback)."""

class Constants(BaseConstants):
    name_in_url = 'single_treatment_public_goods'
    players_per_group = None
    num_rounds = 8

    results_template = 'public_goods/Results_c.html'

    """Amount allocated to each player"""
    max_savings = c(5)
    multiplier = 1


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        savings_session = [p.savings for p in self.get_players() if p.savings != None]
        if savings_session:
            res = {
                'avg_saving': sum(savings_session)/len(savings_session),
                'min_saving': min(savings_session),
                'max_saving': max(savings_session),
            }
        else:
            res = {
                'avg_saving': '(no data)',
                'min_saving': '(no data)',
                'max_saving': '(no data)',
            }
        return res

    def creating_session(self):
        # self.Constants.endowment = self.session.config['endowment']
        # treatments = itertools.cycle(['control', 't1', 't2','t3'])
        endowment = c(self.session.config['endowment'])
        for g in self.get_groups():
            g.com_goal = self.session.config['community_goal_decimal']
        if self.round_number == 1:
            for g in self.get_groups():
                # treatment = next(treatments)

                for p in g.get_players():
                    # p.participant.vars['treat'] = treatment
                    p.treatment = p.participant.vars['treatment']
                    p.participant.vars['endowment'] = endowment
                    p.endowment = p.participant.vars['endowment']

        if self.round_number > 1:
             for p in self.get_players():
                 p.treatment = p.participant.vars['treatment']


class Group(BaseGroup):
    com_goal = models.FloatField(min=0, max=1)
    min_round = models.IntegerField(initial=1, doc="go back to x last round. E.g. 1 for last round")

    def set_payoffs(self):
        people_in_treatment = self.get_players()
        treatments = set([p.treatment for p in people_in_treatment])
        for temp_treatment in treatments:
            treatment_group = [p for p in people_in_treatment if p.treatment == temp_treatment]
            total_people_treatment = len(treatment_group)
            total_savings = (total_people_treatment * self.session.config['endowment']) - sum(
                [p.participant.vars['endowment'] for p in people_in_treatment if p.treatment == temp_treatment])
            shares = total_savings / (total_people_treatment * self.session.config['endowment'])
            avg_savings = total_savings/total_people_treatment
            for p in treatment_group:
                p.participant.vars['endowment'] = p.participant.vars['endowment'] - p.savings
                if self.round_number > self.min_round:
                    p.last_savings = p.in_round(self.round_number - self.min_round).savings
            #if self.com_goal > 0:
                if self.round_number == Constants.num_rounds:
                    if shares >= self.com_goal and self.round_number == Constants.num_rounds:
                            p.participant.vars['endowment'] = (p.participant.vars['endowment']) + (
                                avg_savings * 3)
                            p.endowment = p.participant.vars['endowment']
                else:
                    #for p in treatment_group:
                    #    p.participant.vars['endowment'] = p.participant.vars['endowment'] - p.savings
                        p.endowment = p.participant.vars['endowment']
                        #if self.round_number > self.min_round:
                        #    p.last_savings = p.in_round(self.round_number - self.min_round).savings


class Player(BasePlayer):
    treatment = models.CharField(doc="Treatment of each player")
    endowment = models.CurrencyField(
        min=0,
        doc="endowment by each player"
    )
    savings = models.CurrencyField(
        doc="Savings by each player",widget=widgets.RadioSelectHorizontal,
        label="How much do you choose to contribute to the group energy conservation goal?"
        #,choices=currency_range(c(0), c(0.10), c(0.02))
    )
    financial_reward = models.FloatField(min=0)
    last_savings = models.CurrencyField(initial=0)

