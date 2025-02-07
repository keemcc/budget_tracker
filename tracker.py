class DailyBudget:
    def __init__(self, date = None, allowance = None):
        self.date = date
        self.allowance = allowance
        self.transactions = dict()
        self.remaining = allowance

class Transaction:
    def __init__(self, spent, description = "No description", category = "No category"):
        self.spent = spent
        self.description = description
        self.category = category