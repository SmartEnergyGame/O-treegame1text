from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools

doc = """
        Public good game section (Rounds and feedback).
      """

class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 2
    num_rounds = 2

    instructions_template = 'public_goods/Instructions.html'
    results_template = 'public_goods/Results_control.html'

    """Amount allocated to each player"""
    endowment = c(10)
    max_savings = c(5)
    multiplier = 1


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        savings_session = [p.savings for p in self.get_players() if p.savings != None]
        if savings_session:
            return {
                'avg_saving': sum(savings_session)/len(savings_session),
                'min_saving': min(savings_session),
                'max_saving': max(savings_session),
            }
        else:
            return {
                'avg_saving': '(no data)',
                'min_saving': '(no data)',
                'max_saving': '(no data)',
            }

    def creating_session(self):
        # self.Constants.endowment = self.session.config['endowment']
        treatments = itertools.cycle(['control', 't1', 't2','t3'])
        for g in self.get_groups():
            g.com_goal = self.session.config['community_goal_decimal']
        if self.round_number == 1:
            for g in self.get_groups():
                treatment = next(treatments)

                for p in g.get_players():
                    p.participant.vars['treat'] = treatment
                    p.treat = treatment
        if self.round_number > 1:
            for p in self.get_players():
                p.treat = p.participant.vars['treat']



class Group(BaseGroup):
    com_goal = models.FloatField(min=0, max=1)
    total_savings = models.CurrencyField()
    individual_savings_share = models.FloatField()

    def set_payoffs(self):
        self.total_savings = sum([p.savings for p in self.get_players()]) # C:1 S:4, C:1 S:1, TS:5 SS:5/20 F:
        self.individual_savings_share = self.total_savings / (Constants.players_per_group * Constants.endowment)
        for p in self.get_players():
            p.consumption = Constants.endowment-p.savings
        if self.com_goal > 0:
            if self.individual_savings_share >= self.com_goal:
                for p in self.get_players():
                    p.financial_reward = p.consumption.to_real_world_currency(self.session) + (self.total_savings / Constants.players_per_group).to_real_world_currency(self.session)
            else:
                for p in self.get_players():
                    p.financial_reward = p.consumption.to_real_world_currency(self.session)

# finacial with group
# reward group (1 has nothing ,1 treatment any group reward, 1 emotional reward, group savings x3 and distributed equally,)





class Player(BasePlayer):
    treat = models.CharField(doc="Treatment of each player")
    consumption = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="Consumption by each player"
    )
    savings = models.CurrencyField(min=0, max=Constants.max_savings, doc="Savings by each player",choices=[c(0), c(2), c(4)])
    financial_reward = models.FloatField(min=0)
    last_savings = models.CurrencyField()
