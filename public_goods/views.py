from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    body_text = "Introduction text."
    pass


class Contribute(Page):
    """Player: Choose how much to contribute"""
    months = {1: "January",
              2: "February",
              3: "March",
              4: "April",
              5: "May",
              6: "June",
              7: "July",
              8: "August",
              9: "September",
              10: "October",
              11: "November",
              12: "December"}

    form_model = models.Player
    form_fields = [ 'savings']
    def savings_choices(self):
        return [[c,c.to_real_world_currency(self.session)] for c in currency_range(0, self.session.config['endowment']*.5, 2)]
    #    return currency_range(0, self.player.participant.vars['endowment']*.5, 2)
    def vars_for_template(self):
        month = self.months[self.player.round_number]
        if self.participant.vars['treatment'] == 'DTI':
            injunctive_text = "Remember, contributing to the collective energy conservation goal is important to protect the environment by saving energy from fossil fuels."
        else:
            injunctive_text = ' '
        return {'month': month, 'endowment':self.player.participant.vars['endowment'].to_real_world_currency(self.session),
                'currency': c(1),'real_value':c(1).to_real_world_currency(self.session),'injunctive_text':injunctive_text}


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute."


class Results_c(Page):
    def vars_for_template(self):
            cum_earnings = (sum([sum([p.savings for p in self.group.in_round(round_id).get_players() if p.treatment == self.player.treatment]) for round_id in
                                 range(1, self.player.round_number + 1)])).to_real_world_currency(self.session)
            return {
                'endowment': self.player.participant.vars['endowment'].to_real_world_currency(self.session),
                'savings': self.player.savings.to_real_world_currency(self.session),
                'last_savings': self.player.last_savings.to_real_world_currency(self.session),
                'total_savings': cum_earnings,
            }

    def is_displayed(self):
        if self.participant.vars['treatment'] == 'control':
            return True


class Results_D(Page):
    def vars_for_template(self):
            treatment_group = [p for p in self.group.get_players() if p.treatment == self.player.treatment]
            cum_earnings = (sum([sum([p.savings for p in self.group.in_round(round_id).get_players() if p.treatment == self.player.treatment]) for round_id in
                                 range(1, self.player.round_number + 1)])).to_real_world_currency(self.session)
            parts = [{'id_in_group': p.id_in_group, 'savings': p.savings.to_real_world_currency(self.session)} for p in
                     treatment_group]
            average_savings = sum([p.savings for p in treatment_group ])/len(treatment_group)
            if self.player.savings >= average_savings:
                position = ''' You are above average'''
            else:
                position = ''' You are below average'''
            return {
                'endowment': self.player.participant.vars['endowment'].to_real_world_currency(self.session),
                'savings': self.player.savings.to_real_world_currency(self.session),
                'last_savings': self.player.last_savings.to_real_world_currency(self.session),
                'total_savings': cum_earnings,
                'position': position,
                'parts': parts

            }
    def is_displayed(self):
        if self.participant.vars['treatment'] == 'D':
            return True
class Results_DTI(Page):
    def is_displayed(self):
        if self.participant.vars['treatment'] == 'DTI':
            return True

    def vars_for_template(self):
        treatment_group = [p for p in self.group.get_players() if p.treatment == self.player.treatment]
        cum_earnings = (sum([sum(
            [p.savings for p in self.group.in_round(round_id).get_players() if p.treatment == self.player.treatment])
                             for round_id in
                             range(1, self.player.round_number + 1)])).to_real_world_currency(self.session)
        parts = [{'id_in_group': p.id_in_group, 'savings': p.savings.to_real_world_currency(self.session)} for p in
                 treatment_group]
        average_savings = sum([p.savings for p in treatment_group]) / len(treatment_group)
        if self.player.savings > average_savings:
            position = ''' You are above average'''
        else:
            position = ''' You are below average'''
        return {
            'endowment': self.player.participant.vars['endowment'].to_real_world_currency(self.session),
            'savings': self.player.savings.to_real_world_currency(self.session),
            'last_savings': self.player.last_savings.to_real_world_currency(self.session),
            'total_savings': cum_earnings,
            'position': position,
            'parts': parts

        }

page_sequence = [
    Contribute,
    ResultsWaitPage,
    Results_c,
    Results_D,
    Results_DTI
]
