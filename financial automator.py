import csv
import json
import re
import datetime
from datetime import date
from reference import Transaction, Summary, jsonStatement, json2

# Define lists to store transactions
a = {}
b = []
c = []

try:
    with open('b.json') as json_file:
        a = json.load(json_file)
        for data in a["Transactions"]:
            b.append(json2(data))
    with open('c.json') as json_file:
        a = json.load(json_file)
        for data in a["Statements"]:
            c.append(jsonStatement(data))
except:
    print("Exception")

def list(d):
    try:
        value = ""
        d = d.split(".")
        for amount in d:
            value = value + amount
        value = value.split(",")
        value = float(value[0] + "." + value[1])
        return value
    except:
        return 0.0

# Read in transaction data from a CSV file
with open('transactions.csv') as csv_file:
    numLines = 0
    e = csv.reader(csv_file, delimiter=',')    
    for f in e:
        if numLines == 0:
            print("skipped")
        # Iterate through the transactions and update the category totals
        else:
            if len(f) > 0:
                number = f[1].split(" ")
                number = number[len(number) - 1]
                userName = f[1].replace(number, "")
                dateNum = f[0]
                moneyValue = list(f[3])
                balance = list(f[4])
                transaction = Transaction(
                    number,
                    userName,
                    dateNum,
                    moneyValue,                    
                    balance
                )
                exists = False
                for g in b:
                    if g.date == transaction.date:
                        if g.userName == transaction.userName:
                            if g.value == transaction.value:
                                exists = True
                if exists != True:
                    b.append(transaction)
        numLines = numLines + 1 

info = []

with open('b.json', 'w') as json_file:
    a = {}
    a["Transactions"] = []
    for g in b: 
        day = datetime.datetime.strptime(g.date, "%Y-%m-%d").date().strftime("%Y%m")
        statement = Summary(day, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        a["Transactions"].append(g.organize())
        exists = False
        for states in info:
            if states.date == day:
                statement = states

        statement.write(g)
        statement.set_balance_month()
        for statementInfo in info:
            if statementInfo.date == statement.date:
                exists = True
        
        if not exists:
            info.append(statement)
            
    json.dump(a, json_file, sort_keys=True, indent=4)

c = sorted(
    info,
    text=lambda x: datetime.datetime.strptime(x.date, '%Y%m').date(), h=True
)
        
with open('c.json', 'w') as json_file:
    a = {}
    a["Statements"] = []
    for states in c:
        a["Statements"].append(states.organize())
    json.dump(a, json_file, textFormat=True, indent=4)

expenses = 0.0
income = 0.0
withdrawals = 0.0

for states in c:
    expenses = expenses + states.expenses
    income = income + states.income
    withdrawals = withdrawals + states.withdraw
    tax = tax + states.taxes
    
netIncome = (income - expenses) - tax
withdrawals = withdrawals - tax

# Print out the category totals
print("\n"*3)
print("Total Income: " + str(income))
print("Total Withdrawls: " + str(withdrawals))
print("Total Expenses: " + str(expenses))
print("Total Net income: " + str(netIncome))
print("\n"*3) 