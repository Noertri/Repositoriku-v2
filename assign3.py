class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def deposit(self, amount, desc=""):
        depo = dict()

        depo["amount"] = amount
        depo["description"] = desc

        self.ledger.append(depo)

    def check_funds(self, amount):
        if amount > self.ledger[0]["amount"]:
            return False
        else:
            return True

    def withdraw(self, amount=None, desc=""):
        wdw = dict()

        if not (amount is None) and self.check_funds(amount):
            wdw["amount"] = (-1) * amount
            wdw["description"] = desc
            self.ledger.append(wdw)
            return True
        elif not (amount is None) and not self.check_funds(amount):
            return False
        else:
            return False

    def transfer(self, amount=None, others=None):
        desc_1 = "Transfer to " + others.name
        desc_2 = "Transfer from " + self.name
        if not (amount is None) and self.check_funds(amount):
            self.withdraw(amount=amount, desc=desc_1)
            others.deposit(amount=amount, desc=desc_2)
            return True
        elif not (amount is None) and not self.check_funds(amount):
            return False
        else:
            return False

    def get_balance(self):
        n = len(self.ledger)
        total = self.ledger[0]["amount"]
        for i in range(1, n):
            if self.ledger[i]["amount"] < 0:
                total = total + self.ledger[i]["amount"]

        return total

    def __str__(self):
        n = len(self.ledger)
        line1 = f"{self.name}".center(30, '*') + "\n"
        val = self.ledger[0].values()
        values = list(val)
        line2 = values[1][:23].ljust(23) + f"{values[0]:.2f}".rjust(7) + "\n"
        for i in range(1, n):
            if self.ledger[i]["amount"] < 0:
                val = self.ledger[i].values()
                values = list(val)
                line2 = line2 + values[1][:23].ljust(23) + f"{values[0]:.2f}".rjust(7) + "\n"
        total = self.get_balance()
        line3 = "Total: {0:.2f}".format(total)
        lines = line1 + line2 + line3

        return lines


def create_spend_chart(categories=[]):
    n = len(categories)
    totals = []
    percents = {}
    for i in range(n):
        ledger = categories[i].ledger
        name = categories[i].name
        m = len(ledger)

        tot = 0.
        for j in range(1, m):
            if ledger[j]["amount"] < 0:
                tot = tot + (-1)*ledger[j]["amount"]

        totals.append(tot)
        percents[name] = tot

    total_all = 0.
    for tot in totals:
        total_all += tot

    for k, v in percents.items():
        percents[k] = (v/total_all)*10

    o_charts = {}
    for n, p in percents.items():
        if (p >= 0) and (p < 1):
            o_charts[n] = 'o'
        elif (p >= 1) and (p < 2):
            o_charts[n] = 2*'o'
        elif (p >= 2) and (p < 3):
            o_charts[n] = 3*'o'
        elif (p >= 3) and (p < 4):
            o_charts[n] = 4*'o'
        elif (p >= 4) and (p < 5):
            o_charts[n] = 5*'o'
        elif (p >= 5) and (p < 6):
            o_charts[n] = 6*'o'
        elif (p >= 6) and (p < 7):
            o_charts[n] = 7*'o'
        elif (p >= 7) and (p < 8):
            o_charts[n] = 8*'o'
        elif (p >= 8) and (p < 9):
            o_charts[n] = 9*'o'
        elif (p >= 9) and (p < 10):
            o_charts[n] = 10*'o'
        else:
            o_charts[n] = 11*'o'

    points = list(o_charts.values())
    n1 = len(points)

    full_chart = "Percentage spent by category\n"
    for i in range(10, -1, -1):
        full_chart += f"{i*10}".rjust(3) + "| "
        for j in range(n1):
            points[j] = points[j].ljust(11)
            full_chart += points[j][i] + "  "
            if j == (n1-1):
                full_chart += "\n"

    full_chart += "    -" + n1*"---" + "\n"

    labels = list(o_charts.keys())
    n2 = len(labels)

    labels_length = []
    for i in range(n2):
        le = len(labels[i])
        labels_length.append(le)

    m2 = max(labels_length)

    label_lines = []
    for i in range(m2):
        lin = " "*5
        for j in range(n2):
            labels[j] = labels[j].ljust(m2)
            lin += labels[j][i] + "  "
        label_lines.append(lin)

    full_chart = full_chart + "\n".join(label_lines)

    return full_chart


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)

print(create_spend_chart([food, clothing, auto]))