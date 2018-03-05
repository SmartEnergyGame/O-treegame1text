from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    name_in_url = 'post_survey'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    #def creating_session(self):
    #    for g in self.get_groups():
    #        for p in g.get_players():
    #            p.treatment = p.participant.vars['treatment']
    #            p.endowment = p.participant.vars['endowment']
    #            p.correct_answers = p.participant.vars['correct_answers']
    #            if 'correct_answers' in p.participant.vars:
    #                print("+++++++++++++++++++++++in participant vars")
    #            else:
    #                print("not correct_ans")
    pass



class Group(BaseGroup):
    def get_bonus(self):
        endowments = [p.participant.vars['endowment'] for p in self.get_players()]
        total_savings = len(endowments) * self.session.config['endowment'] - sum(endowments)
        group_goal = (.5 * 8 * len(endowments))
        f = total_savings * 3
        indv_shares = f / len(endowments)
        for p in self.get_players():
            p.correct_answers = p.participant.vars['correct_answers']
            if total_savings >= group_goal:
                    p.bonus = indv_shares
                    print(p.correct_answers)
                    p.total_payment = p.participant.vars['endowment'] + p.bonus + c(p.participant.vars['correct_answers'] * .5)
            else:
                p.bonus = c(0)
                p.total_payment = p.participant.vars['endowment'] + c(p.participant.vars['correct_answers'] * .5)


class Player(BasePlayer):
    bonus = models.CurrencyField(min=0)
    
    total_payment = models.CurrencyField(min=0)
    treatment = models.CharField(
            doc="Treatment of each player"
        )

    savings = models.CurrencyField(
        doc="Savings by each player",
        widget=widgets.RadioSelectHorizontal,
        label="How much do you choose to contribute to the group energy conservation goal?"
        #,choices=currency_range(c(0), c(0.10), c(0.02))
    )
    financial_reward = models.FloatField(min=0)
    last_savings = models.CurrencyField(initial=0)
    q1 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],widget=widgets.RadioSelectHorizontal,
        label="Plants"
    )
    q2 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="Marine life"
    )
    q3 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="Birds"
    )
    q4 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="Animals"
    )
    q5 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="My prosperity"
    )
    q6 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="My lifestyle"
    )
    q7 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="My health"
    )
    q8 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="My future"
    )
    q9 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="People in my community"
    )
    q10 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="The human race"
    )
    q11 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="Children"
    )
    q12 = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelectHorizontal,
        label="People in the United States"
    )
    q021 = models.IntegerField(
        doc="Question 1", 
        label="What is your year of birth?",min=1918,max=2010
    )
    q031 = models.CharField(
        doc="Question 1",
        label="What is your sex? ",widget=widgets.RadioSelectHorizontal,
        choices=[
            ['M', "Male"],
            ['F', "Female"]
        ]
    )
    q041 = models.CharField(
        doc="Question 1", 
        label="What term best describes your ethnic identity?",
        choices=[
            ['AFA', "African-American "], 
            ['ASA', "Asian-American "],
            ['H', "HISPANIC "],
            ['W', "WHITE"],
            ['NA', "NATIVE AMERICAN"]
        ],widget=widgets.RadioSelectHorizontal,
    )
    q051 = models.CharField(
        doc="Question 1", 
        label="What country or region were you born?",
        choices=[
            ['AFA', "North America"],
            ['ASA', "Central/South America"],
            ['H', "Australia/New Zealand "],
            ['W', "Africa"], 
            ['NA', "South-East Asia"],
            ['NA', "South Asia"], 
            ['NA', "Other Asia"], 
            ['NA', "Western Europe"],
            ['NA', "Northern Europe"], 
            ['NA', "Eastern Europe"]
        ]
    )
    q061 = models.CharField(
        doc="Question 1", 
        label="How long have you live in the United States?",widget=widgets.RadioSelectHorizontal,
        choices=[
            ['0', "Less than 1 year"]
            ,['1', "1-2 years"],
            ['2', "2-5 years"],

            ['3', "More than 5 years"]
        ]
    )
    q071 = models.CharField(
        doc="Question 1", 
        label="Where did you live when you were 15 years old?",
        choices=[
            ['1', "In the countryside but not on a farm"],
            ['2', "On a farm"],
            ['3', "Small city or town (under 50,000)"]
        ],widget=widgets.RadioSelectHorizontal,
    )
    q081 = models.CharField(
        doc="Question 1", 
        label="What is your political party affiliation, if any?",
        choices=[
            ['1', "Democrat"],
            ['2', "Independent"],
            ['3', "Republican"],
            ['4', "None"],
        ],widget=widgets.RadioSelectHorizontal,
    )
    q091 = models.CharField(
        doc="Question 1", 
        label="Do you consider yourself an environmentalist?",
        choices=[
            ['Y', "Yes"],
            ['N', "No"]
        ],widget=widgets.RadioSelectHorizontal,
    )
    q101 = models.CharField(
        doc="Question 1", 
        label="What year are you in your undergraduate studies?",
        choices=[
            ['1', "First"],
            ['2', "Second"],
            ['3', "Third"],
            ['4', "Fourth"],
            ['5', "Fifth or higher"],
        ],widget=widgets.RadioSelectHorizontal,
    )
    q111 = models.CharField(
        doc="Question 1", 
        label="What is your main field of study at Purdue?",
        choices=[
            ['1', "Agriculture/Natural Resources"],
            ['2', "Business/Economics"],
            ['3', "Education"],
            ['4', "Engineering"],
            ['5', "Health Sciences"],
            ['6', "Liberal Arts"],
            ['7', "Science"],
            ['8', "Technology"],

        ]
    )
    q121 = models.CharField(
        doc="Question 1",
        label="How many experiments have you participated in before this one?",
        choices=[
            ['1','None'],
            ['2','1 - 2 previous'],
            ['3','3 - 5 previous'],
            ['4','More than 5 previous'],
        ],widget=widgets.RadioSelectHorizontal,
    )
    q131 = models.CharField(
        doc="Question 1",
        label="Are you currently receiving some form of financial assistance for your educational expenses?",
        choices=[
            ['Y', "Yes"],
            ['N', "No"]
        ],widget=widgets.RadioSelectHorizontal,
    )
    q141 = models.IntegerField(
        doc="Question 1",
        label="Are you currently employed in a job while in school?  If so, please indicate how many hours per week on average you work.  If you study full time and do not work, enter 0.",min=0,max=168

    )
    treatment = models.CharField(doc="Treatment")

