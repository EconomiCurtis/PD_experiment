from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Decision(Page):
    form_model = models.Player
    form_fields = ['action','guess']

    def guess_max(self):
        return self.session.vars['num_subjects']-1

    def vars_for_template(self):
        return {
            'p11': Constants.payoff_matrix[str(self.round_number)]['X']['X'],
            'p12': Constants.payoff_matrix[str(self.round_number)]['X']['Y'],
            'p21': Constants.payoff_matrix[str(self.round_number)]['Y']['X'],
            'p22': Constants.payoff_matrix[str(self.round_number)]['Y']['Y'],
            'num_other_players': len(self.subsession.get_players()) - 1
        }


class DecisionWaitPage(WaitPage):
    template_name = 'coordination/DecisionWaitPage.html'
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        for g in self.subsession.get_groups():
            g.interact()
            print('players have interacted!')

    def vars_for_template(self):
        return {
            'p11': Constants.payoff_matrix[str(self.round_number)]['X']['X'],
            'p12': Constants.payoff_matrix[str(self.round_number)]['X']['Y'],
            'p21': Constants.payoff_matrix[str(self.round_number)]['Y']['X'],
            'p22': Constants.payoff_matrix[str(self.round_number)]['Y']['Y'],
            'num_other_players': len(self.subsession.get_players()) - 1
        }

class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'paying_round': self.session.vars['paying_round'],
            'action': self.player.participant.vars['action_PartII'],
            'other_action': self.player.participant.vars['other_action_PartII'],
            'guess': self.player.participant.vars['guess_PartII'],
            'otherX': self.player.participant.vars['otherX_PartII'],
            'payoff_from_guess': self.player.participant.vars['payoff_from_guess'],
            'payoff_from_action': self.player.participant.vars['payoff_from_action'],
            'payoff_PartII': self.player.participant.vars['payoff_from_guess']+self.player.participant.vars['payoff_from_action']
        }


class MyWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        if self.round_number == Constants.num_rounds:
            for p in self.subsession.get_players():
                p.participant.vars['payoff_coordination'] = sum([this_player.payoff for this_player in p.in_all_rounds()])
                print((p,sum([this_player.payoff for this_player in p.in_all_rounds()])),p.participant.vars['payoff_coordination'])


page_sequence = [
    Decision,
    DecisionWaitPage,
    Results,
    MyWaitPage
]