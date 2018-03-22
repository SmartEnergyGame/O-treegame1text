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
        min=1,max=7,
        label="Plants",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                             "Plants"
    )
    q2 = models.IntegerField(
        min=1,max=7,
        label="Marine life",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                                  "Marine life"
    )
    q3 = models.IntegerField(
        min=1,max=7,
        label="Birds",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                            "Birds"
    )
    q4 = models.IntegerField(
        min=1,max=7,
        label="Animals",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                              "Animals"
    )
    q5 = models.IntegerField(
        min=1,max=7,
        label="My prosperity",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                                    "My prosperity"
    )
    q6 = models.IntegerField(
        min=1,max=7,
        label="My lifestyle",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                                   "My lifestyle"
    )
    q7 = models.IntegerField(
        min=1,max=7,
        label="My health",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                                "My health"
    )
    q8 = models.IntegerField(
        min=1,max=7,
        label="My future",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                                "My future"
    )
    q9 = models.IntegerField(
        min=1,max=7,
        label="People in my community",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                                             "People in my community"
    )
    q10 = models.IntegerField(
        min=1,max=7,
        label="The human race",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                                     "The human race"
    )
    q11 = models.IntegerField(
        min=1,max=7,
        label="Children",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                               "Children"
    )
    q12 = models.IntegerField(
        min=1,max=7,
        label="People in the United States",doc = "People often express concern about environmental problems, but some people differ as to which consequences concern them the most. We are going to list different areas where environmental problems could have harmful consequences.  For each, please rate how concerned you are about their impact using a scale from 1 to 7. If you are not at all concerned, give the area a rating of 1. If you are extremely concerned, give it a rating of 7. Of course, you can choose any number between 1 and 7 for your answer. Answer:"
                                                  "People in the United States"
    )
    q021 = models.IntegerField(
        doc="What is your year of birth?",
        label="What is your year of birth?",min=1918,max=2010
    )
    q031 = models.CharField(
        doc="What is your sex?",
        label="What is your sex? ",widget=widgets.RadioSelectHorizontal,
        choices=[
            ['M', "Male"],
            ['F', "Female"]
        ]
    )
    q041 = models.CharField(
        doc="What term best describes your ethnic identity?",
        label="What term best describes your ethnic identity?",
        choices=[
            "African-American ",
            "Asian-American ",
            "Hispanic",
            "White",
            "Native American",
            "Other"
        ],widget=widgets.RadioSelectHorizontal,
    )
    q042 = models.CharField(
        doc="If the answer to the previous question was 'Other' please fill the box with the term that best describes your ethnic identity: ",
        label="If the answer to the previous question was 'Other' please fill the box with the term that best describes your ethnic identity: ",blank=True
    )
    q051 = models.CharField(
        doc="What country or region were you born?",
        label="What country or region were you born?",
        choices=[
            "North America",
            "Central/South America",
            "Australia/New Zealand ",
            "Africa",
            "Asia",
            "Europe",
            "Other"
        ],widget=widgets.RadioSelectHorizontal,
    )
    q052 = models.CharField(
        doc="If the answer to the previous question was 'Other' please fill the box with your country.",
        label="If the answer to the previous question was 'Other' please fill the box with your country.",blank = True
    )
    q061 = models.CharField(
        doc="How long have you live in the United States?",
        label="How long have you live in the United States?",widget=widgets.RadioSelectHorizontal,
        choices=[
            "More than 5 years",
            "2-5 years",
            "1-2 years",
            "Less than 1 year"
        ]
    )
    q071 = models.CharField(
        doc="Where did you live when you were 15 years old?",
        label="Where did you live when you were 15 years old?",
        choices=[
            "In the countryside but not on a farm",
            "On a farm",
            "Small city or town (under 50,000)",
            "Medium size city (50,000-250,000)",
            "Suburb near a large city",
            "Large city (250,000-3,000,000)",
            "Very large city (over 3,000,000)"

        ]
    )
    q081 = models.CharField(
        doc="What is your political party affiliation, if any?",
        label="What is your political party affiliation, if any?",
        choices=[
            "Democrat",
            "Independent",
            "Republican",
            "None",
            "Other",
        ],widget=widgets.RadioSelectHorizontal,
    )
    q082 = models.CharField(
        doc="If the answer to the previous question was 'Other' please fill the box with the other political party affiliation of your preference.",
        label="If the answer to the previous question was 'Other' please fill the box with the other political party affiliation of your preference.",blank=True

    )
    q091 = models.CharField(
        doc="Do you consider yourself an environmentalist?",
        label="Do you consider yourself an environmentalist?",
        choices=[
            "Yes",
            "No"
        ],widget=widgets.RadioSelectHorizontal,
    )
    q101 = models.CharField(
        doc="What year are you in your undergraduate studies?",
        label="What year are you in your undergraduate studies?",
        choices=[
            "First",
            "Second",
            "Third",
            "Fourth",
            "Fifth or higher",
        ],widget=widgets.RadioSelectHorizontal,
    )
    q111 = models.CharField(
        doc="What is your main field of study at Purdue?",
        label="What is your main field of study at Purdue?",
        choices=[
            "Agriculture/Natural Resources",
            "Business/Economics",
            "Education",
            "Engineering",
            "Health Sciences",
            "Liberal Arts",
            "Science",
            "Technology",
            "Other"

        ]
    )
    q112 = models.CharField(
        doc="If the answer to the previous question was 'Other' please fill the box with the other main field of study at Purdue",
        label="If the answer to the previous question was 'Other' please fill the box with the other main field of study at Purdue", blank=True

    )
    q121 = models.CharField(
        doc="How many experiments have you participated in before this one?",
        label="How many experiments have you participated in before this one?",
        choices=[
            'None',
            '1 - 2 previous',
            '3 - 5 previous',
            'More than 5 previous',
        ],widget=widgets.RadioSelectHorizontal,
    )
    q131 = models.CharField(
        doc="Are you currently receiving some form of financial assistance for your educational expenses?",
        label="Are you currently receiving some form of financial assistance for your educational expenses?",
        choices=[
            "Yes",
            "No"
        ],widget=widgets.RadioSelectHorizontal,
    )
    q141 = models.IntegerField(
        doc="Are you currently employed in a job while in school?  If so, please indicate how many hours per week on average you work.  If you study full time and do not work, enter 0.",
        label="Are you currently employed in a job while in school?  If so, please indicate how many hours per week on average you work.  If you study full time and do not work, enter 0.",min=0,max=168

    )
    treatment = models.CharField(doc="Treatment")

    q151 = models.CharField( label = "During the experiment, which of the following reasons were you given to contribute to the conservation account?",choices = ["Reducing energy consumption reduces pollution and threat of global warming.",
                                                                                                                                                                  "Reducing energy consumption reduces our reliance on imported fossil fuels.",
                                                                                                                                                                  "Reducing energy consumption is important to improve the local economy."])


