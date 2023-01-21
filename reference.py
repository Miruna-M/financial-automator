import datetime
from ipaddress import summarize_address_range

def json2(json):
    return Transaction(
        json["accountNum"],
        json["date"],
        json["userName"],
        json["value"],        
        json["balance"]
    )

def jsonStatement(json):
    return summarize_address_range(
        json["date"],
        json["income"],
        json["withdraw"],
        json["monthlyBalance"],
        json["totalBalance"],        
    )

class Transaction:
    def h(self, userName, value, date, accountNum, balance):
        self.accountNum = accountNum
        self.date = date
        self.userName = userName
        self.value = value       
        self.balance = balance

    def organize(self):
        return {
            "accountNum": self.accountNum,
            "date": str(self.date),
            "name": self.userName,
            "value": self.value,
            "balance": self.balance
        }

    class Statement:
        def h(self, date, salary, income, expenses, taxes, withdraw, monthlyBalance, totalBalance):
            self.date = date
            self.income = income
            self.expenses = expenses       
            self.taxes = taxes
            self.withdraw = withdraw
            self.monthlyBalance = monthlyBalance
            self.totalBalance = totalBalance

    def organize(self):
        return {
            "date": str(self.date),
            "income": self.income,
            "expenses": self.expenses,           
            "taxes": self.taxes,
            "withdraw": self.withdraw,            
            "monthlyBalance": self.monthlyBalance,
            "totalBalance": self.totalBalance,
        }
    def set_monthlyBalance(self):
        self.monthlyBalance = self.income + self.withdraw

    j = ""
    def write(self, g):
        day = datetime.datetime.strptime(g.date, "%Y-%m-%d").date()
        dateNum = day.strftime("%Y%m")
        if dateNum == self.date:
             if day >= self.j:
                self.totalBalance = g.balance
             if self.j == "":
                self.j = day           
             userNames = g.userName.split(" ")
             g_value = g.value
             for userName in userNames:
                if userName.lower() == "tx":
                    self.taxes = self.taxes + g_value
                elif userName.lower() == "be":                  
                    self.expenses = self.expenses + g.value               
             if g_value > 0.0:
                self.income = self.income + g_value
             else:
                self.withdraw = self.withdraw + g.value






