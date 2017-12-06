from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random



#role specific instructions
#class InstructionsCompany(Page):
class FirstWaitPage(WaitPage):
    title_text = "Waiting for other participants to join study session"
    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1

class InstructionsCompanyNew(Page):
    def is_displayed(self):
        return self.player.role() == 'company' and self.round_number == 1
class InstructionsCompany2(Page):
    def is_displayed(self):
        return self.player.role() == 'company' and self.round_number == 1

class InstructionsCustomer(Page):
    def is_displayed(self):
        return self.player.role() == 'customer' and self.round_number == 1
class InstructionsCustomer2(Page):
    def is_displayed(self):
        return self.player.role() == 'customer' and self.round_number == 1

# comprehension questions for everyone
class ComprehensionCheck1(Page):
    def is_displayed(self):
        return self.round_number == 1
    # only allow participant to proceed if they get all answers correct (inifinite tries)
    def error_message(self, values):
        if values["compre_workernumber"] != 5:
            return 'You did not answer question 1 correctly.'
        if values["compre_workercharacteristic"] != 'Favorite Food':
            return 'You did not answer question 2 correctly.'
        if values["compre_workerpayment"] != 'The 5 workers the Customer selects will be paid':
            return 'You did not answer question 3 correctly.'

    form_model = models.Player
    form_fields = ['compre_workernumber', 'compre_workercharacteristic', 'compre_workerpayment']


#comprehension questions for company role
class ComprehensionCheck2_Company(Page):
    def is_displayed(self):
        return self.player.role() == 'company' and self.round_number == 1
    #only allow participant to proceed if they get all answers correct (inifinite tries)
    def error_message(self, values):
        if values["compre_yourbonus"] != 'I will receive $0.20 for every Customer that selects me in the randomly chosen round':
            return 'You did not answer question 1 correctly.'
        if values["compre_customerchoose"] != 'They select 1 Company, which is made up of 5 workers':
            return 'You did not answer question 2 correctly.'
        if values["compre_roundpayment"] != 'One that is randomly chosen at the end of the study':
            return 'You did not answer question 3 correctly.'
        if values["compre_changerounds"] != 'Yes':
            return 'You did not answer question 4 correctly.'
    form_model = models.Player
    form_fields = ['compre_yourbonus', 'compre_customerchoose', 'compre_roundpayment','compre_changerounds']

#comprehension questions for customer role
class ComprehensionCheck2_Customer(Page):
    def is_displayed(self):
        return self.player.role() == 'customer' and self.round_number == 1
    #only allow participant to proceed if they get all answers correct (inifinite tries)
    def error_message(self, values):
        if values["compre_customerbonus"] != 'Company will receive $0.20 for if I select them in the randomly chosen round':
            return 'You did not answer question 1 correctly.'
        if values["compre_youchoose"] != 'I choose 1 Company, which is made up of 5 workers':
            return 'You did not answer question 2 correctly.'
        if values["compre_roundpayment"] != 'One that is randomly chosen at the end of the study':
            return 'You did not answer question 3 correctly.'
        if values["compre_changerounds"] != 'Yes':
            return 'You did not answer question 4 correctly.'
    form_model = models.Player
    form_fields = ['compre_customerbonus', 'compre_youchoose', 'compre_roundpayment','compre_changerounds']

class ReminderPage(Page):
    def is_displayed(self):
        return self.round_number == 1

#transition page
class Before_MathQuestions(Page):
    def is_displayed(self):
        return self.round_number == 1

#page with sample math questions
class MathQuestion_Samples(Page):
    def is_displayed(self):
        return self.round_number == 1

#show all potential workers to company
class Show_All_Workers_Company(Page):
    def is_displayed(self):
        return self.player.role() == 'company' and self.round_number == 1
# show all potential workers to customer
class Show_All_Workers_Customer(Page):
    def is_displayed(self):
        return self.player.role() == 'customer' and self.round_number == 1

#company chooses its 7 workers
class Offer(Page):
    def is_displayed(self):
        return self.player.role() == 'company'
    #display error message if don't choose right number of employees
    def error_message(self, values):
        if values["hire_emp1"] + values["hire_emp2"] + values["hire_emp3"] + values["hire_emp4"] + values["hire_emp5"] + values["hire_emp6"]+values["hire_emp7"]+values["hire_emp8"]+values["hire_emp9"]+values["hire_emp10"]!= 5:
            return 'You must hire exactly 5 workers'
    def vars_for_template(self):
        employee_dict = Constants.employee_IDs.copy()
        random.shuffle(employee_dict)
        employees = []
        for i in employee_dict:
            employees.append((i, Constants.company_choose_employee_choices[i]))
        return {'employees': employees}
        #'numbers': range(1,len(Constants.company_choose_employee_choices)+1)
    form_model = models.Player
    form_fields = ['hire_emp{}'.format(i) for i in range(1, len(Constants.company_choose_employee_choices)+1)]

class OfferWaitPage(WaitPage):
    def vars_for_template(self):
        if self.player.role() == 'customer':
            body_text = "You are the customer. Waiting for company to choose its workers."
        else:
            body_text = "Waiting for other Companies to choose its workers and the Customers to decide on a Company."
        return {'body_text': body_text}


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Accept(Page):

    #Customer must choose a Company.
    def error_message(self, values):
        if values["customer_choose_company"] <0:
            return 'You must select a Company.'
        if values["customer_choose_company"] > Constants.number_of_companies:
            return 'You must select a single Company.'
    def vars_for_template(self):
        for p in self.group.get_players():
            chosen = []
            if p.role() == 'company':
                if p.hire_emp1 == 1:
                     chosen.append(Constants.company_choose_employee_choices[1])
                if p.hire_emp2 == 1:
                    chosen.append(Constants.company_choose_employee_choices[2])
                if p.hire_emp3 == 1:
                    chosen.append(Constants.company_choose_employee_choices[3])
                if p.hire_emp4 == 1:
                    chosen.append(Constants.company_choose_employee_choices[4])
                if p.hire_emp5 == 1:
                    chosen.append(Constants.company_choose_employee_choices[5])
                if p.hire_emp6 == 1:
                    chosen.append(Constants.company_choose_employee_choices[6])
                if p.hire_emp7 == 1:
                    chosen.append(Constants.company_choose_employee_choices[7])
                if p.hire_emp8 == 1:
                    chosen.append(Constants.company_choose_employee_choices[8])
                if p.hire_emp9 == 1:
                    chosen.append(Constants.company_choose_employee_choices[9])
                if p.hire_emp10 == 1:
                    chosen.append(Constants.company_choose_employee_choices[10])
            p.company_choose_employee = chosen

        #return sorted values for each company decision
        sorted_company_choices = sorted(p.company_choose_employee for p in self.group.get_players() if p.role() == 'company')
        return {'sorted_company_choices': sorted_company_choices, 'companies': Constants.customer_choose_company_choices}

    def is_displayed(self):
        return self.player.role() == 'customer'

    form_model = models.Player
    form_fields = ['customer_choose_company']




class Results(Page):
    def is_displayed(self):
        return self.round_number != Constants.num_rounds

    def vars_for_template(self):
        #return sorted values for each company decision
        for p in self.group.get_players():
            chosen = []
            if p.role() == 'company':
                if p.hire_emp1 == 1:
                     chosen.append(Constants.company_choose_employee_choices[1])
                if p.hire_emp2 == 1:
                    chosen.append(Constants.company_choose_employee_choices[2])
                if p.hire_emp3 == 1:
                    chosen.append(Constants.company_choose_employee_choices[3])
                if p.hire_emp4 == 1:
                    chosen.append(Constants.company_choose_employee_choices[4])
                if p.hire_emp5 == 1:
                    chosen.append(Constants.company_choose_employee_choices[5])
                if p.hire_emp6 == 1:
                    chosen.append(Constants.company_choose_employee_choices[6])
                if p.hire_emp7 == 1:
                    chosen.append(Constants.company_choose_employee_choices[7])
                if p.hire_emp8 == 1:
                    chosen.append(Constants.company_choose_employee_choices[8])
                if p.hire_emp9 == 1:
                    chosen.append(Constants.company_choose_employee_choices[9])
                if p.hire_emp10 == 1:
                    chosen.append(Constants.company_choose_employee_choices[10])
            p.company_choose_employee = chosen

        #return sorted values for each company decision
        sorted_company_choices = sorted(p.company_choose_employee for p in self.group.get_players() if p.role() == 'company')
        return {'sorted_company_choices': sorted_company_choices, 'companies': Constants.customer_choose_company_choices, 'next_round': self.round_number + 1}



class OverallResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'received': self.player.payoff - Constants.base_pay,
            #'effort_cost': cost_from_effort(self.group.agent_work_effort),
        }


class Demographics(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = models.Player
    form_fields = ['age',
                   'gender']

class LastPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    FirstWaitPage,
    InstructionsCompanyNew,
    InstructionsCompany2,
    InstructionsCustomer,
    InstructionsCustomer2,
    ComprehensionCheck1,
    ComprehensionCheck2_Company,
    ComprehensionCheck2_Customer,
    ReminderPage,
    Before_MathQuestions,
    MathQuestion_Samples,
    Show_All_Workers_Company,
    Show_All_Workers_Customer,
    Offer,
    OfferWaitPage,
    Accept,
    ResultsWaitPage,
    Results,
    OverallResults,
    Demographics,
    LastPage
]

