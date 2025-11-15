from app.triggers.instt_expense_triggers import expense_triggers
from app.triggers.instt_income_triggers import income_triggers
from app.models.account_orm import account_table



def main_triggers():
    account_table()
    expense_triggers()
    # income_triggers()




if __name__=="__main__":
    main_triggers()