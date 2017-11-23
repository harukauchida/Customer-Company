from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_principal_agent'
    players_per_group = 2
    num_rounds = 3

    instructions_template = 'my_principal_agent/Instructions.html'
    base_pay = c(5)
    company_chosen_pay = c(2)
    company_rejected_pay = c(0)
    #rn customer gets 1 if choose company since there is only 1 company
    customer_choose_pay = c(1)
    customer_reject_pay = c(0)

    company_choose_employee_choices = [
        [percent / 100.0, '{}%'.format(percent)]
        for percent in range(10, 100 + 1, 10)]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    company_chosen = models.BooleanField(
        doc="""Whether customer chooses company""",
        widget=widgets.RadioSelect(),
        choices=(
            (True, 'Choose'),
            (False, 'Decline'),
        )
    )

    company_choose_employee = models.FloatField(
        choices=Constants.company_choose_employee_choices,
        doc="""Company's different options of employee to offer customer""",
        verbose_name='Company Hiring Options',
        widget=widgets.RadioSelectHorizontal()
    )
    def set_payoffs(self):
        company = self.get_player_by_role('company')
        customer = self.get_player_by_role('customer')
        if not self.contract_accepted:
            company.payoff = Constants.company_rejected_pay
            customer.payoff = Constants.customer_choose_pay
        else:
            company.payoff = Constants.company_chosen_pay
            customer.payoff = Constants.customer_reject_pay
        customer.payoff += Constants.base_pay
        company.payoff += Constants.base_pay




class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'customer'
        if self.id_in_group == 2:
            return 'company'
