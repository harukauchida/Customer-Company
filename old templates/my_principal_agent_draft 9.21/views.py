from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass

class Offer(Page):
    def is_displayed(self):
        return self.player.role() == 'company'

    form_model = models.Group
    form_fields = ['company_choose_employee']

class OfferWaitPage(WaitPage):
    def vars_for_template(self):
        if self.player.role() == 'customer':
            body_text = "You are the customer. Waiting for company to choose its employees."
        else:
            body_text = "Waiting for customer."
        return {'body_text': body_text}


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Accept(Page):
    def is_displayed(self):
        return self.player.role() == 'customer'

    form_model = models.Group
    form_fields = ['company_chosen']


    #timeout_submission = {
    #    'company_chosen': False,
    #    'agent_work_effort': 1,
    #}



class Results(Page):
    def vars_for_template(self):
        return {
            'received': self.player.payoff - Constants.base_pay,
            #'effort_cost': cost_from_effort(self.group.agent_work_effort),
        }

page_sequence = [
    Introduction,
    Offer,
    Accept,
    ResultsWaitPage,
    Results
]
