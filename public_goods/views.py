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
    months = {
        1: "January",
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
        12: "December"
    }

    form_model = models.Player
    form_fields = [ 'savings']
    def savings_choices(self):
        return [[c,c.to_real_world_currency(self.session)] for c in currency_range(0, 4, 2)]
    #    return currency_range(0, self.player.participant.vars['endowment']*.5, 2)
    def vars_for_template(self):
        month = self.months[self.player.round_number]
        if self.participant.vars['treatment'] == 'DTI':
            if self.player.participant.vars['role'] == 'type1':
                injunctive_text = "Remember, contributing to the collective energy conservation goal is important to to help reduce air and water pollution creating health problems affecting you and your family and improve your chances of gaining a larger share of the conservation account funds."
            elif self.player.participant.vars['role'] == 'type2':
                injunctive_text = "Remember, contributing to the collective energy conservation goal is important to to help reduce air and water pollution creating health problems affecting your community and improve everyone’s chances of gaining a larger share of the conservation account funds."
            else:
                injunctive_text = ''
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
            res =  {
                'endowment': self.player.participant.vars['endowment'].to_real_world_currency(self.session),
                'savings': self.player.savings.to_real_world_currency(self.session),
                'last_savings': self.player.last_savings.to_real_world_currency(self.session),
                'total_savings': cum_earnings,
                'goal':self.session.config['community_goal_decimal']*100,
            }
            return res

    def is_displayed(self):
        if self.participant.vars['treatment'] == 'control':
            return True


class Results_D(Page):
    def vars_for_template(self):
            treatment_group = [p for p in self.group.get_players() if p.treatment == self.player.treatment]
            cum_earnings = (sum([sum([p.savings for p in self.group.in_round(round_id).get_players() if p.treatment == self.player.treatment]) for round_id in
                                 range(1, self.player.round_number + 1)])).to_real_world_currency(self.session)
            parts = [{'id_in_group': treatment_group.index(p), 'savings': p.savings.to_real_world_currency(self.session)} for p in
                     treatment_group]
            average_savings = sum([p.savings for p in treatment_group ])/len(treatment_group)
            parts_savings = [p.savings.to_real_world_currency(self.session) for p in
                     treatment_group]
            parts_labels = ["participant "+str(label) for label in range(len(treatment_group))]
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
                'parts': parts,
                'parts_savings': parts_savings,
                'parts_label': parts_labels,
                'goal':self.session.config['community_goal_decimal']*100,
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
        parts = [{'id_in_group':  treatment_group.index(p), 'savings': p.savings.to_real_world_currency(self.session)} for p in
                 treatment_group]
        average_savings = sum([p.savings for p in treatment_group]) / len(treatment_group)
        parts_savings = [p.savings.to_real_world_currency(self.session) for p in
                         treatment_group]
        parts_labels = ["participant " + str(label) for label in range(len(treatment_group))]
        if self.player.savings >= average_savings:
            position = ''' You are above average'''
        else:
            position = ''' You are below average'''
        if self.player.participant.vars['role'] == 'type1':
            injunctive_label = "Remember, contributing to the collective energy conservation goal is important to to help reduce air and water pollution creating health problems affecting you and your family and improve your chances of gaining a larger share of the conservation account funds."
        elif self.player.participant.vars['role'] == 'type2':
            injunctive_label = "Remember, contributing to the collective energy conservation goal is important to to help reduce air and water pollution creating health problems affecting your community and improve everyone’s chances of gaining a larger share of the conservation account funds."
        else:
            injunctive_label = ''

        return {
            'endowment': self.player.participant.vars['endowment'].to_real_world_currency(self.session),
            'savings': self.player.savings.to_real_world_currency(self.session),
            'last_savings': self.player.last_savings.to_real_world_currency(self.session),
            'total_savings': cum_earnings,
            'position': position,
            'parts': parts,
                'parts_savings': parts_savings,
                'parts_label': parts_labels,
            'injunctive_label': injunctive_label,
            'goal':self.session.config['community_goal_decimal']*100,
        }

page_sequence = [
    Contribute,
    ResultsWaitPage,
    Results_c,
    Results_D,
    Results_DTI
]
