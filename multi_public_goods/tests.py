from otree.api import (
    Currency as c, currency_range, SubmissionMustFail, Submission
)
from . import views
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    cases = ['basic', 'min', 'max']
    def play_round(self):
        case = self.case
        yield (views.Introduction)
        if case == 'basic' and self.player.id_in_group == 1:
            for invalid_contribution in [-1, 101]:
                yield SubmissionMustFail(views.Contribute, {
                    'contribution': invalid_contribution})

        contribution = {
            'min': 0,
            'max': 100,
            'basic': 50,
        }[case]

        yield (views.Contribute, {"contribution": contribution})
        yield (views.Results)

        expected = {"min":100, "max":200}
        if self.player.id_in_group == 1:
            if case == "min" or case == "max":
                expected_payoff = expected[case]
            else:
                expected_payoff = 150
            assert self.player.payoff == expected_payoff
