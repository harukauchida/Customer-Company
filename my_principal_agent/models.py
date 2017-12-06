from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
#from django import forms
import random


author = 'Haruka 2017'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_principal_agent'
    #make sure to change number of participants in settings.py if change here
    players_per_group = 7
    number_of_companies = 2
    # add 1 to the number of times have customer choose workers
    num_rounds = 10 + 1

    instructions_template = 'my_principal_agent/Instructions.html'
    all_workers_template = 'my_principal_agent/All_Workers.html'
    base_pay = c(3)
    company_chosen_pay = c(0.2)
    company_rejected_pay = c(0)
    random_round_for_payment = 2
    #rn customer gets 1 no matter what
    customer_choose_pay = c(0.05)

    #employee choices
    company_choose_employee_choices ={
        1: '<20, M, Running>',
        2: '<21, F, Reading>',
        3: '<22, F, Photography>',
        4: '<21, M, Dancing>',
        5: '<22, M, Hiking>',
        6: '<23, F, Running>',
        7: '<20, F, Dancing>',
        8: '<21, M, Writing>',
        9: '<22, F, Reading>',
        10: '<22, M, Cooking>'
    }
    #list of key numbers for employee choices
    employee_IDs = list(company_choose_employee_choices.keys())

    #number of companies
    customer_choose_company_choices = [1, 2]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    #def CompChooseEmployees(self):
    #    buyer = self.get_player_by_role('company')
    #    print(Group.company_choose_employee)

    #company_choose_employee = models.CharField(
    #    choices=Constants.company_choose_employee_choices,
    #    doc="""Company's different options of employee to offer customer""",
    #    verbose_name='Company Hiring Options',
    #    widget=widgets.RadioSelectHorizontal()
        #widget=forms.CheckboxSelectMultiple()
    #)


    def set_payoffs(self):
        #use random_round_for_payment'th round to determine payoff
        players = self.get_players()
        company = [p for p in players if p.role() == 'company']
        customer = [p for p in players if p.role() != 'company']

        #every customer's choice
        company_choices = [p.customer_choose_company for p in customer]
        #all chosen companies (eliminate redundance from company_choices)
        company_chosen = [p for p in company if p.id_in_group in company_choices]

        #for every company that was chosen by a customer
        for p in company_chosen:
            p.is_chosen = True
            p.chosen_number = 0
            #loop over every customer
            for choose_once in customer:
                #if that customer chose that company
                if choose_once.customer_choose_company == p.id_in_group:
                    #add one
                    p.chosen_number +=1
        #only calculate payoffs for specified round
        #p.chosen_number represents how many times that company was chosen in that round
        #if self.round_number == Constants.random_round_for_payment:
            #calculate payment for chosen companies
        for p in players:
            if p in company:
                if p in company_chosen:
                        #company payment is proportional to chosen number
                    p.payoff = Constants.company_chosen_pay * p.chosen_number
                else:
                    p.payoff = Constants.company_rejected_pay
                #if is not a company (is a customer), get paid customer_choose_pay
            else:
                p.payoff = Constants.customer_choose_pay




class Player(BasePlayer):
    def role(self):
        #if id is over number_of_companies, then is customer.
        #number_of_companies companies, players_per_group - number_of_companies customers.
        if self.id_in_group > Constants.number_of_companies:
            return 'customer'
        return 'company'

    is_chosen = models.BooleanField(initial=False)

    chosen_number = models.PositiveIntegerField(initial=0)

    hire_emp1 = models.BooleanField()
    hire_emp2 = models.BooleanField()
    hire_emp3 = models.BooleanField()
    hire_emp4 = models.BooleanField()
    hire_emp5 = models.BooleanField()
    hire_emp6 = models.BooleanField()
    hire_emp7 = models.BooleanField()
    hire_emp8 = models.BooleanField()
    hire_emp9 = models.BooleanField()
    hire_emp10 = models.BooleanField()

    #worker_1 = models.CharField()
    #worker_2 = models.CharField()
    #worker_3 = models.CharField()

    compre_workernumber = models.PositiveIntegerField(
        choices=[1, 2, 3, 5, 9],
    )
    compre_workercharacteristic = models.CharField(
        choices=['Age', 'Gender', 'Hobby', 'Favorite Food'],
        widget=widgets.RadioSelect()
    )
    compre_workerpayment = models.CharField(
        choices=['All will be paid', 'The 5 workers the Customer selects will be paid'],
        widget=widgets.RadioSelect()
    )

    compre_yourbonus = models.CharField(
        choices=['I will receive $0.20 for every Customer that selects me in the randomly chosen round', 'I will receive $0.20 for every Customer that selects me in every round'],
        widget=widgets.RadioSelect()
    )
    compre_customerchoose = models.CharField(
        choices=['They are assigned 5 workers', 'They select 1 Company, which is made up of 5 workers'],
        widget=widgets.RadioSelect()
    )
    compre_roundpayment = models.CharField(
        choices=['First round', 'One that is randomly chosen at the end of the study', 'Last round'],
        widget=widgets.RadioSelect()
    )
    compre_changerounds = models.CharField(
        choices=['Yes', 'No'],
        widget=widgets.RadioSelect()
    )
    compre_customerbonus = models.CharField(
        choices=['Company will receive $0.20 for if I select them in the randomly chosen round', 'Company will receive $0.20 for every round I select them in'],
        widget=widgets.RadioSelect()
    )
    compre_youchoose = models.CharField(
        choices=['I am assigned 5 workers', 'I choose 1 Company, which is made up of 5 workers'],
        widget=widgets.RadioSelect()
    )


    company_choose_employee = models.CharField()

    #company_choose_employee = models.CharField(
    #    choices=Constants.company_choose_employee_choices,
    #    doc="""Company's different options of employee to offer customer""",
    #    verbose_name='Company Hiring Options',
    #    widget=widgets.RadioSelectHorizontal()
    #)

    #customer indicates which company they prefer
    customer_choose_company = models.PositiveIntegerField()
    #    choices=[(i, 'Choose Company %i' % i) for i in
    #             range(1, Constants.players_per_group)],
    #    doc="""Whether customer chooses company""",
    #    verbose_name='Please choose which company you like most',
    #    widget=widgets.RadioSelectHorizontal(),
    #)
    age = models.PositiveIntegerField(
        verbose_name='What is your age?',
        min=18, max=99)

    gender = models.CharField(
        choices=['Male', 'Female'],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect())